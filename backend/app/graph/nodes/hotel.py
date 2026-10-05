from config import get_llm
from app.graph.state import TravelState
from app.tools.web_search import web_search
from langchain_core.messages import HumanMessage

llm = get_llm()

tools = [web_search]

llm_with_tools = llm.bind_tools(tools)


def hotel_researcher(state: TravelState) -> dict:

    print("\n==============================")
    print("HOTEL RESEARCHER")
    print("==============================")

    destination = state.get("destination")
    start_date = state.get("start_date")
    end_date = state.get("end_date")
    adults = state.get("adults")
    children = state.get("children")
    budget = state.get("budget")
    preferences = state.get("preferences", [])

    prompt = f"""
You are only a hotel research agent.
Find suitable accommodation options for the trip.

Destination:
{destination}

Dates:
{start_date} to {end_date}

Travelers:
{adults} adults and {children} children

Total trip budget (in INR):
{budget}

Preferences:
{preferences}

Search for suitable family-friendly hotels or accommodations
in {destination}.

You MUST NOT:
- create an itinerary
- research flights
- research trains
- research attractions
- create a travel guide
- create packing lists
- provide general travel advice

Return concise research only.

Focus on the following aspects of accommodation:
- location
- suitability as per budget and preferences
- proximity to important attractions
- vegetarian/ non-vegetarian friendly surroundings where relevant
- approximate price information if available
- suitability for the overall budget

Use web search to find current information.

Do not invent hotel prices, availability, ratings, or facilities.
If information is unavailable, say so.

Provide enough information for another agent to select
appropriate accommodation.


"""

    messages = state.get("hotel_messages", [])

    if not messages:
        messages = [
            HumanMessage(content=prompt)
        ]

    response = llm_with_tools.invoke(messages)

    print("\nHotel research response:")
    print(response)

    return {
        "hotel_messages": [response]
    }