from datetime import datetime, timedelta

from app.graph.state import TravelState


def date_processor(state: TravelState) -> dict:

    print("\n==============================")
    print("DATE PROCESSOR")
    print("==============================")

    start_date = state.get("start_date")
    end_date = state.get("end_date")
    trip_duration = state.get("trip_duration")

    # If end date is already available, nothing needs to be calculated.
    if end_date:
        print(f"End date already provided: {end_date}")

        return {}

    # If we have duration, calculate end date.
    if start_date and trip_duration:

        start = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        )

        # A 5-day trip starting Dec 20:
        # Day 1 = Dec 20
        # Day 5 = Dec 24
        #
        # Therefore we add duration - 1 days.

        calculated_end = start + timedelta(
            days=trip_duration - 1
        )

        calculated_end_date = calculated_end.strftime(
            "%Y-%m-%d"
        )

        print(
            f"Calculated end date: {calculated_end_date}"
        )

        return {
            "end_date": calculated_end_date
        }

    print("Unable to calculate end date.")

    return {}