from config import get_llm
from app.graph.state import TravelState
from app.models.travel import TravelRequest

llm = get_llm()

structured_llm = llm.with_structured_output(TravelRequest)

def request_analyzer(state: TravelState) -> dict:

    user_request = state["user_request"]
    user_clarification = state.get("user_clarification")

    if user_clarification:

        combined_request = f"""
        Original travel request:

        {user_request}

        Additional information provided by the user:

        {user_clarification}
        """
    else:
        combined_request = user_request

    print("\n==============================")
    print("REQUEST ANALYZER")
    print("==============================")

    print(f"Combined request: {combined_request}")

    prompt = f"""
You are a travel request analysis agent.

Your job is to extract structured travel information from
the user's request.

Extract only information explicitly provided by the user.

Do NOT invent:
- dates
- duration
- budget
- number of travelers
- preferences
- origin
- destination

If information is not available, return null for that field.

If the user explicitly says something like:
- "5 day trip"
- "for one week"
- "3 nights and 4 days"

extract the trip duration.

Do not calculate an end date from the duration.

If both a start date and end date are explicitly provided,
extract both.

User request:

{combined_request}
"""

    travel_request = structured_llm.invoke(prompt)

    print("\nExtracted travel request:")
    print(travel_request)

    return travel_request.model_dump()