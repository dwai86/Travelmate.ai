from config import get_llm
from app.graph.state import TravelState
from app.models.travel import ValidationResult


llm = get_llm()

structured_llm = llm.with_structured_output(
    ValidationResult
)


def validator(state: TravelState) -> dict:

    print("\n==============================")
    print("VALIDATOR")
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
    itinerary = state.get("itinerary")

    print(f"Destination: {destination}")
    print(f"Dates: {start_date} to {end_date}")
    print(f"Travelers: {adults} adults, {children} children")
    print(f"Budget: {budget}")
    print(f"Preferences: {preferences}")

    prompt = f"""
You are a travel plan validation agent.

Your job is to validate the generated travel itinerary
against the original trip requirements and available research.

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


GENERATED ITINERARY

{itinerary}


Validate the itinerary using the following criteria:

1. DATE CONSISTENCY
   - The itinerary should cover the complete trip period.
   - Dates should be in the correct sequence.

2. TRAVELER REQUIREMENTS
   - The itinerary should be reasonable for the specified
     number of adults and children.

3. PREFERENCE ALIGNMENT
   - The itinerary should respect the user's preferences.
   - Vegetarian preferences should not be violated.
   - Temple and spiritual interests should be appropriately
     represented.

4. TRANSPORT CONSISTENCY
   - Transportation mentioned in the itinerary should be
     consistent with the available transport research.
   - Do not assume specific transport details that are not
     present in the research.

5. RESEARCH GROUNDING
   - The itinerary should not introduce unsupported facts.
   - Do not consider information valid merely because it
     sounds plausible.

6. GENERAL QUALITY
   - The itinerary should be practical and coherent.
   - Identify obvious inconsistencies or missing information.

If the itinerary satisfies the requirements:

valid = true

If there are significant problems:

valid = false

Put the specific problems in "issues".

Put useful improvements or suggestions in "recommendations".

Do not invent facts while validating.
"""

    validation_result = structured_llm.invoke(prompt)

    print("\nValidation Result:")
    print(validation_result)

    return {
        "validation_result": validation_result
    }