from config import get_llm
from app.models.travel import Itinerary

from app.graph.state import TravelState

llm = get_llm()

structured_llm = llm.with_structured_output(
    Itinerary
)


def itinerary_planner(state: TravelState) -> dict:

    print("\n==============================")
    print("ITINERARY PLANNER")
    print("==============================")

    origin = state.get("origin")
    destination = state.get("destination")
    start_date = state.get("start_date")
    end_date = state.get("end_date")

    adults = state.get("adults")
    children = state.get("children")

    budget = state.get("budget")
    preferences = state.get("preferences", [])

    destination_research = state.get("destination_research")
    transport_options = state.get("transport_options")

    hotel_options = state.get("hotel_options")

    print(f"Origin: {origin}")
    print(f"Destination: {destination}")
    print(f"Dates: {start_date} to {end_date}")
    print(f"Travelers: {adults} adults, {children} children")
    print(f"Budget: {budget}")
    print(f"Preferences: {preferences}")

    prompt = f"""
You are a travel itinerary planning agent.

Create a practical day-wise itinerary for the trip.

TRIP DETAILS

Origin:
{origin}

Destination:
{destination}

Start date:
{start_date}

End date:
{end_date}

Travelers:
{adults} adults and {children} children

Budget:
{budget}

Preferences:
{preferences}


DESTINATION RESEARCH

{destination_research}


TRANSPORT RESEARCH

{transport_options}

HOTEL RESEARCH

{hotel_options}


Create a practical itinerary for the entire trip.

Consider:
- the exact travel dates
- number and type of travelers
- temples and spiritual places
- vegetarian preferences
- reasonable travel time
- the available transport information
- the provided hotel information
- the research provided above

Use ONLY the information supported by the destination research
, transport research and hotel research. Do not invent any information.

If a detail such as price, departure time, duration, availability,
or opening time is not present in the research, do not invent it.
Do not claim that a hotel is booked or that availability
is confirmed unless the research explicitly confirms it.

When information is unavailable, omit that detail rather than
making an assumption.

Do not convert a general transport recommendation
into a confirmed booking or confirmed availability.

For example, if research says flights are generally
recommended but does not confirm availability for the
specific travel date, describe it as a recommendation
rather than a confirmed travel arrangement.

Organize the itinerary day by day.
"""

    structured_response = structured_llm.invoke(prompt)

    print("\nItinerary:")
    print(structured_response)

    return {
        "itinerary": structured_response
    }