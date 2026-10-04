from config import get_llm
from app.graph.state import TravelState
from app.models.travel import HotelResearch
from langchain_core.messages import AIMessage

llm = get_llm()

structured_llm = llm.with_structured_output(
    HotelResearch
)


def hotel_formatter(state: TravelState) -> dict:

    print("\n==============================")
    print("HOTEL FORMATTER")
    print("==============================")

    messages = state.get("hotel_messages", [])

    if not messages:
        return {"hotel_options": None}

    final_message = None

    for message in reversed(messages):
        if isinstance(message, AIMessage) and not message.tool_calls:
            final_message = message
            break

    if final_message is None:
        return {"hotel_options": None}

    prompt = f"""
You are a hotel research formatter.

Convert the following hotel research into structured information.

Do not invent information.

Hotel research:

{final_message.content}
"""

    structured_hotel = structured_llm.invoke(prompt)

    print("\nStructured hotel research:")
    print(structured_hotel)

    return {
        "hotel_options": structured_hotel
    }