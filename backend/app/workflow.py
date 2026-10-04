from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode

from app.graph.state import TravelState
from app.graph.nodes.request_analyzer import request_analyzer
from app.graph.nodes.requirements_checker import requirements_checker
from app.graph.nodes.date_processor import date_processor
from app.graph.nodes.human_input import human_input
from app.graph.nodes.researcher import researcher
from app.tools.web_search import web_search
from app.tools.place_search import place_search
from app.graph.nodes.research_formatter import research_formatter
from app.graph.nodes.transport import  transport_researcher
from app.graph.nodes.transport_formatter import transport_formatter
from app.graph.nodes.itinerary import itinerary_planner
from app.graph.nodes.validator import validator
from app.graph.nodes.hotel import hotel_researcher
from app.graph.nodes.hotel_formatter import hotel_formatter



def hotel_router(state: TravelState):

    messages = state.get("hotel_messages", [])

    if not messages:
        return "end"

    last_message = messages[-1]

    if last_message.tool_calls:
        return "tool"

    return "end"

def validator_router(state: TravelState):

    validation_result = state.get("validation_result")

    if validation_result and validation_result.valid:
        return "valid"

    return "invalid"

def research_router(state: TravelState):

    messages = state.get("research_messages", [])

    if not messages:
        return "end"

    last_message = messages[-1]

    if last_message.tool_calls:
        return "tool"

    return "end"

def transport_router(state: TravelState):

    messages = state.get("transport_messages", [])

    if not messages:
        return "end"

    last_message = messages[-1]

    if last_message.tool_calls:
        return "tool"

    return "end"


def requirements_router(state: TravelState):

    if state.get("requirements_complete"):
        return "complete"

    return "incomplete"


def build_graph():

    workflow = StateGraph(TravelState)

    research_tool_node = ToolNode([web_search, place_search], messages_key="research_messages")
    transport_tool_node = ToolNode([web_search], messages_key="transport_messages")
    hotel_tool_node = ToolNode([web_search], messages_key="hotel_messages")

    # Add node
    workflow.add_node(
        "request_analyzer",
        request_analyzer
    )

    workflow.add_node(
        "requirements_checker",
        requirements_checker
    )

    workflow.add_node(
        "human_input",
        human_input
    )

    workflow.add_node(
            "date_processor",
            date_processor
        )

    workflow.add_node("researcher", researcher)

    workflow.add_node("research_tools", research_tool_node)

    workflow.add_node(
    "transport_tools",
    transport_tool_node
    )

    workflow.add_node(
    "research_formatter",
    research_formatter
    )

    workflow.add_node("hotel_researcher", hotel_researcher)
    workflow.add_node("hotel_formatter", hotel_formatter)
    workflow.add_node("hotel_tools", hotel_tool_node)

    workflow.add_node("transport_researcher", transport_researcher)

    workflow.add_node(
    "transport_formatter",
    transport_formatter
    )


    workflow.add_node(
        "itinerary_planner",
        itinerary_planner
        )

    workflow.add_node("validator", validator)

    # START → request_analyzer
    workflow.add_edge(
        START,
        "request_analyzer"
    )

    # request_analyzer → requirements_checker
    workflow.add_edge(
        "request_analyzer",
        "requirements_checker"
    )

    # requirements_checker → END
    workflow.add_conditional_edges(
    "requirements_checker",
    requirements_router,
    {
        "complete": "date_processor",
        "incomplete": "human_input"
    }
    )

    workflow.add_edge(
            "human_input",
            "request_analyzer"
        )

    # -------------------------
    # Date Processor
    # -------------------------

    workflow.add_edge("date_processor", "researcher")
    workflow.add_edge("date_processor", "transport_researcher")
    workflow.add_edge("date_processor", "hotel_researcher")

    workflow.add_conditional_edges(
    "hotel_researcher",
    hotel_router,
    {
        "tool": "hotel_tools",
        "end": "hotel_formatter"
    }
    )

    workflow.add_edge(
    "hotel_tools",
    "hotel_researcher"
    )

    workflow.add_conditional_edges(
    "researcher",
    research_router,
    {
        "tool": "research_tools",
        "end": "research_formatter"
    }
    )



    workflow.add_conditional_edges(
        "transport_researcher",
        transport_router,
        {
            "tool": "transport_tools",
            "end": "transport_formatter"
        }
        )

    workflow.add_edge("research_tools", "researcher")

    workflow.add_edge("transport_tools", "transport_researcher")

    workflow.add_edge("research_formatter", "itinerary_planner")

    workflow.add_edge("transport_formatter", "itinerary_planner")

    workflow.add_edge("hotel_formatter", "itinerary_planner")

    workflow.add_edge("itinerary_planner", "validator")

    workflow.add_conditional_edges(
    "validator",
    validator_router,
    {
        "valid": END,
        "invalid": END
    }
    )

    checkpointer = InMemorySaver()
    return workflow.compile(checkpointer=checkpointer)