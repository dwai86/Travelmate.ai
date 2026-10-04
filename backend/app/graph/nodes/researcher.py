from config import get_llm
from app.graph.state import TravelState
from app.tools.web_search import web_search
from app.tools.place_search import place_search
from datetime import datetime
from langchain_core.messages import HumanMessage

def extract_month_name(date_string: str) -> str | None:
    """Parses a YYYY-MM-DD string and returns the full month name."""
    if not date_string:
        return None
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    return date_obj.strftime("%B")


llm = get_llm()
tools = [web_search, place_search]
llm_with_tools = llm.bind_tools(tools)


def researcher(state: TravelState) -> dict:

    print("\n==============================")
    print("DESTINATION RESEARCHER")
    print("==============================")

    destination = state.get("destination")
    start_date = state.get("start_date")
    end_date = state.get("end_date")
    preferences = state.get("preferences", [])

    month_name = extract_month_name(start_date)

    messages = state.get("research_messages", [])

    print(f"Destination: {destination}")
    print(f"Travel dates: {start_date} to {end_date}")
    print(f"Preferences: {preferences}")
    print(f"Month: {month_name}")


    prompt = f"""
You are a destination research agent.

Research and summarize the destination for a travel planning system.

Destination:
{destination}

Travel dates:
{start_date} to {end_date}

Travel month:
{month_name}

Traveler preferences:
{preferences}

You have access to two tools:

1. web_search
   Use this for current destination information,
   attractions, cultural information, travel tips,
   events, etc.

2. place_search
   Use this when you need to find specific real-world
   places such as restaurants, temples, attractions,
   museums, markets, hotels or other points of interest.

Research:

1. Important places to visit
2. Cultural or spiritual attractions
3. Recommended activities
4. Local travel considerations
5. Places relevant to the traveler's preferences
6. Any important travel tips

Use the appropriate tools when necessary.

You may use one tool or multiple tools depending
on what information is required.

Do not invent facts.
"""

    # First time entering researcher
    if not messages:

        messages = [
            HumanMessage(content=prompt)
        ]


    response = llm_with_tools.invoke(messages)

    print("\nResearch completed:")
    print(response)

    return {
    "research_messages": [response]
    }