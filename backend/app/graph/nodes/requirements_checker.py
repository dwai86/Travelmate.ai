from app.graph.state import TravelState


def requirements_checker(state: TravelState) -> dict:

    print("\n==============================")
    print("REQUIREMENTS CHECKER")
    print("==============================")

    required_fields = [
        "origin",
        "destination",
        "start_date",
        "adults",
        "budget"
    ]

    missing_fields = []

    for field in required_fields:

        value = state.get(field)

        if value is None:
            missing_fields.append(field)

    # Either end_date OR trip_duration must be available
    if state.get("end_date") is None and state.get("trip_duration") is None:
        missing_fields.append("end_date_or_trip_duration")

    if missing_fields:

        print("Missing information:")
        print(missing_fields)

        return {
            "missing_fields": missing_fields,
            "requirements_complete": False
        }

    print("All required information is available.")

    return {
        "missing_fields": [],
        "requirements_complete": True
    }