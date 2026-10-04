from app.workflow import build_graph
from pprint import pprint
from langgraph.types import Command


def main():

    graph = build_graph()

    # --------------------------------
    # Conversation / thread ID
    # --------------------------------

    config = {
        "configurable": {
            "thread_id": "travel-demo-001"
        }
    }

    initial_state = {
        "user_request": (
            "I want to visit Varanasi from Kolkata."
        )
    }

    result = graph.invoke(initial_state, config=config)

    print("\n==============================")
    print("GRAPH PAUSED")
    print("==============================")

    pprint(result)

    # --------------------------------
    # User clarification
    # --------------------------------

    user_response = ("""
        Plan a 5-day family trip from Kolkata to Varanasi starting
20 December 2026. We are 2 adults and 1 child with a budget of ₹60,000. We are vegetarian and particularly interested in temples
and spiritual places."""
    )

    print("\n==============================")
    print("USER PROVIDES CLARIFICATION")
    print("==============================")

    print(user_response)

    # --------------------------------
    # Resume graph
    # --------------------------------

    result = graph.invoke(
        Command(resume=user_response),
        config=config
    )

    print("\n==============================")
    print("FINAL GRAPH STATE")
    print("==============================")

    pprint(result)


if __name__ == "__main__":
    main()