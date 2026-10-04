from config import get_llm

from app.graph.state import TravelState
from app.models.travel import TransportResearch

from langchain_core.messages import AIMessage


llm = get_llm()

structured_llm = llm.with_structured_output(
    TransportResearch
)


def transport_formatter(state: TravelState) -> dict:

    print("\n==============================")
    print("TRANSPORT FORMATTER")
    print("==============================")

    messages = state.get("transport_messages", [])

    if not messages:
        return {
            "transport_options": None
        }

    # Find the latest AIMessage that contains
    # the final research answer, not a tool call.
    final_message = None

    for message in reversed(messages):

        if isinstance(message, AIMessage) and not message.tool_calls:
            final_message = message
            break

    if final_message is None:
        return {
            "transport_options": None
        }

    research_text = final_message.content

    print("\nTransport research received:")
    print(research_text)

    prompt = f"""
You are a transport research formatter.

Convert the following transport research into
structured information.

Extract:

1. Available transport options
2. Approximate travel duration
3. Suitability for the travelers
4. Overall recommendation
5. Important considerations

Do not invent information.

Transport research:

{research_text}
"""

    structured_transport = structured_llm.invoke(prompt)

    print("\nStructured transport research:")
    print(structured_transport)

    return {
        "transport_options": structured_transport
    }