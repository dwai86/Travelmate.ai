from config import get_llm

from app.graph.state import TravelState
from app.tools.web_search import web_search

from langchain_core.messages import HumanMessage


llm = get_llm()

tools = [web_search]

llm_with_tools = llm.bind_tools(tools)


def transport_researcher(state: TravelState) -> dict:

    print("\n==============================")
    print("TRANSPORT RESEARCHER")
    print("==============================")

    origin = state.get("origin")
    destination = state.get("destination")
    start_date = state.get("start_date")
    end_date = state.get("end_date")
    adults = state.get("adults")
    children = state.get("children")
    budget = state.get("budget")

    prompt = f"""
You are ONLY a transport research agent.

Research transportation options for this trip.

Origin:
{origin}

Destination:
{destination}

Travel dates:
{start_date} to {end_date}

Travelers:
{adults} adults and {children} children

Total trip budget (in INR):
{budget}

Research the following:

1. Flights
2. Trains
3. Buses or other practical options
4. Approximate travel duration
5. Important considerations for a family traveler
6. Approximate costs for each option (exact price not required, but provide a reasonable range)
7. Suitability of each option as per the traveler's preferences and budget.

Use the web_search tool when current information
is required. Feel free to investigate multiple sources or invoke the tool multiple times to provide a comprehensive overview.

Do not invent transport schedules or prices.

Provide a useful comparison of the available options.

Do NOT:
- create an itinerary. The Itinery agent will later create the final itinerary based on your research.
- research hotels
- research attractions
- provide a general travel guide

Return concise transport research.
"""

    messages = state.get("transport_messages", [])

    if not messages:
        messages = [
            HumanMessage(content=prompt)
        ]

    response = llm_with_tools.invoke(messages)

    print("\nTransport research response:")
    print(response)

    return {
        "transport_messages": [response]
    }