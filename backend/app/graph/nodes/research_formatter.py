from config import get_llm

from app.graph.state import TravelState
from app.models.travel import DestinationResearch
from langchain_core.messages import AIMessage


llm = get_llm()

structured_llm = llm.with_structured_output(
    DestinationResearch
)


def research_formatter(state: TravelState) -> dict:

    print("\n==============================")
    print("RESEARCH FORMATTER")
    print("==============================")

    messages = state.get("research_messages", [])

    if not messages:
        return {
            "destination_research": None
        }

    # The last AIMessage should contain the final
    # researcher's answer.
    final_message = None

    for message in reversed(messages):
        if isinstance(message, AIMessage):
            final_message = message
            break

    if final_message is None:
        return {
            "destination_research": None
        }

    research_text = final_message.content

    print("\nResearch received:")
    print(research_text)

    prompt = f"""
You are a travel research formatter.

Convert the following destination research into
structured information.

Extract:

1. Important places to visit
2. Recommended activities
3. Travel tips
4. Places or activities that match the traveler's preferences

Do not invent information.

Research:

{research_text}
"""

    structured_research = structured_llm.invoke(prompt)

    print("\nStructured research:")
    print(structured_research)

    return {
    "destination_research": structured_research
    }