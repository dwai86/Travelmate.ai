from langgraph.types import interrupt

from app.graph.state import TravelState


def human_input(state: TravelState) -> dict:

    print("\n==============================")
    print("HUMAN INPUT REQUIRED")
    print("==============================")

    missing_fields = state.get(
        "missing_fields",
        []
    )

    message = (
        "I need some additional information before "
        "I can plan your trip.\n\n"
        f"Missing information: {missing_fields}\n\n"
        "Please provide the missing details."
    )

    # Pause the LangGraph execution and wait for user input
    user_response = interrupt(message)

    print("\nUser clarification received:")
    print(user_response)

    return {
        "user_clarification": user_response
    }