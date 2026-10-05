from typing import Any, List, Optional
from uuid import uuid4
from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator

from app.workflow import build_graph
from config import get_llm

from time import time
from fastapi import HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Travelmate.ai API",
    description="Create travel plans with the Travelmate.ai agent.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

RATE_LIMIT = 1
WINDOW_SECONDS = 2 * 60

request_log = {}

graph = build_graph()


class TravelPlanRequest(BaseModel):

    origin: str = Field(
        min_length=1,
        description="Starting city or place"
    )

    destination: str = Field(
        min_length=1,
        description="Primary destination"
    )

    start_date: date = Field(
        description="Trip start date in YYYY-MM-DD format"
    )

    end_date: date = Field(
        description="Trip end date in YYYY-MM-DD format"
    )

    adults: int = Field(
        ge=1,
        description="Number of adult travelers"
    )

    children: int = Field(
        ge=0,
        description="Number of child travelers"
    )

    budget: float = Field(
        ge=0,
        description="Maximum total trip budget"
    )

    preferences: List[str] = Field(
        default_factory=list,
        description="Travel preferences and constraints"
    )

    food_preference: str = Field(
        description="Food preference: vegetarian or non-vegetarian"
    )

    @model_validator(mode="after")
    def validate_trip_request(self) -> "TravelPlanRequest":

        if self.end_date < self.start_date:
            raise ValueError(
                "end_date must be on or after start_date."
            )

        if self.food_preference.lower() not in {
            "vegetarian",
            "non-vegetarian",
        }:
            raise ValueError(
                "food_preference must be either "
                "'vegetarian' or 'non-vegetarian'."
            )

        total_words = sum(
        len(p.split())
        for p in self.preferences
        )

        if total_words > 50:
            raise ValueError(
                "Preferences cannot exceed 50 words."
            )

        return self


class TravelPlanResponse(BaseModel):

    status: str

    trip: dict[str, Any]

    itinerary: Optional[dict[str, Any]] = None

    transport_options: Optional[dict[str, Any]] = None

    hotel_options: Optional[dict[str, Any]] = None

    validation: Optional[dict[str, Any]] = None


def _model_dict(value: Any) -> Optional[dict[str, Any]]:

    if value is None:
        return None

    if isinstance(value, BaseModel):
        return value.model_dump()

    raise TypeError(
        f"Expected a Pydantic model or None, "
        f"got {type(value).__name__}."
    )


@app.get("/health")
def health_check() -> dict[str, str]:

    return {"status": "ok"}


@app.get("/health/llm")
def llm_health_check():

    try:
        llm = get_llm()

        llm.invoke("Respond with OK.")

        return {
            "status": "ok",
            "llm": "available"
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="LLM service is currently unavailable."
        )

@app.post("/run", response_model=TravelPlanResponse)
def run_travel_agent(
    request: TravelPlanRequest,
    http_request: Request
) -> TravelPlanResponse:
    """
    Run the travel-planning graph for the supplied trip details.
    """

    #### Rate Limiting ####
    client_ip = http_request.client.host

    now = time()

    timestamps = request_log.get(client_ip, [])

    # Remove requests older than 10 minutes
    timestamps = [
        timestamp
        for timestamp in timestamps
        if now - timestamp < WINDOW_SECONDS
    ]

    if len(timestamps) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=(
                "Rate limit exceeded. "
                "Please try again after some time."
            )
        )

    timestamps.append(now)

    request_log[client_ip] = timestamps

    # ----------------------------------------
    # Calculate trip duration
    # Include both start and end dates
    # ----------------------------------------

    trip_duration = (
        request.end_date - request.start_date
    ).days + 1

    # ----------------------------------------
    # Build preferences
    # ----------------------------------------

    preferences = list(request.preferences)

    food_preference = request.food_preference.lower()

    preferences.append(
        f"food preference: {food_preference}"
    )

    # ----------------------------------------
    # Build user request for the agent
    # ----------------------------------------

    preferences_text = ", ".join(preferences)

    user_request = (
        f"Plan a trip from {request.origin} "
        f"to {request.destination}. "

        f"Start date: {request.start_date}. "

        f"End date: {request.end_date}. "

        f"Trip duration: {trip_duration} days. "

        f"Adults: {request.adults}. "

        f"Children: {request.children}. "

        f"Budget: {request.budget}. "

        f"Preferences: {preferences_text}."
    )

    # ----------------------------------------
    # Build initial graph state
    # ----------------------------------------

    trip_details = request.model_dump()

    # Add calculated duration to graph state
    trip_details["trip_duration"] = trip_duration

    # Replace original preferences with the
    # preferences including food preference
    trip_details["preferences"] = preferences

    initial_state = {
        **trip_details,
        "user_request": user_request,
    }

    # ----------------------------------------
    # Create unique graph execution/thread
    # ----------------------------------------

    config = {
        "configurable": {
            "thread_id": str(uuid4())
        }
    }

    # ----------------------------------------
    # Execute LangGraph
    # ----------------------------------------
    try:
        result = graph.invoke(
            initial_state,
            config=config
        )
    except Exception as e:
        print(f"Travel planning error: {type(e).__name__}: {e}")

        raise HTTPException(
            status_code=503,
            detail=f"Travel planning failed: {type(e).__name__}"
        ) from e

    # ----------------------------------------
    # Return clean API response
    # ----------------------------------------

    return TravelPlanResponse(

        status="completed",

        trip={
            "origin": result.get("origin"),
            "destination": result.get("destination"),
            "start_date": result.get("start_date"),
            "end_date": result.get("end_date"),
            "trip_duration": result.get("trip_duration"),
            "adults": result.get("adults"),
            "children": result.get("children"),
            "budget": result.get("budget"),
            "preferences": result.get("preferences", []),
        },

        itinerary=_model_dict(
            result.get("itinerary")
        ),

        transport_options=_model_dict(
            result.get("transport_options")
        ),

        hotel_options=_model_dict(
            result.get("hotel_options")
        ),

        validation=_model_dict(
            result.get("validation_result")
        ),
    )