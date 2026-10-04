from typing import TypedDict, List, Dict, Any, Optional, Annotated
from langgraph.graph.message import add_messages
from app.models.travel import DestinationResearch, HotelResearch, TransportResearch
from app.models.travel import ValidationResult


class TravelState(TypedDict, total=False):

    # -------------------------
    # User request
    # -------------------------
    user_request: str

    # -------------------------
    # Parsed travel information
    # -------------------------
    origin: str
    destination: str

    start_date: str
    end_date: Optional[str]
    trip_duration: Optional[int]

    adults: int
    children: int

    budget: float

    preferences: List[str]

    # -------------------------
    # Agent outputs
    # -------------------------
    destination_research: Optional[DestinationResearch]

    transport_options: Optional[TransportResearch]

    hotel_options: List[Dict[str, Any]]

    itinerary: Optional[str]

    budget_breakdown: Dict[str, Any]

    # -------------------------
    # Validation
    # -------------------------
    validation_result: Optional[ValidationResult]

    validation_attempts: int

    # -------------------------
    # Final response
    # -------------------------
    final_plan: Dict[str, Any]

    # -------------------------
    # Requirement validation
    # -------------------------
    missing_fields: List[str]

    requirements_complete: bool

    user_clarification: Optional[str]

    # -------------------------
    # Human approval
    # -------------------------
    human_approved: bool

    hotel_options: Optional[HotelResearch]

    hotel_messages: Annotated[list, add_messages]

    messages: Annotated[list, add_messages]

    research_messages: Annotated[list, add_messages]
    transport_messages: Annotated[list, add_messages]