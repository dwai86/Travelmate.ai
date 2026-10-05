import os
from datetime import date, timedelta
from typing import Any

import requests
import streamlit as st


st.set_page_config(
    page_title="Travelmate.ai | Your next journey",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_URL = os.getenv("TRAVELMATE_API_URL", "http://127.0.0.1:8000/run")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #142d3d;
        --muted: #637887;
        --teal: #087e83;
        --teal-dark: #075c64;
        --sand: #f4f7f5;
        --line: #dce8e6;
    }
    .stApp {
        background:
            radial-gradient(ellipse at 92% 0%, rgba(37, 160, 152, .13), transparent 34rem),
            linear-gradient(180deg, #f8fbf9 0%, #f2f7f5 100%);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3, [data-testid="stMetricValue"] {
        font-family: 'Manrope', sans-serif !important;
        color: var(--ink);
    }
    .block-container { max-width: 1120px; padding-top: 2rem; padding-bottom: 4rem; }
    .brand {
        color: var(--teal-dark); font-weight: 800; letter-spacing: .08em;
        font-size: .82rem; text-transform: uppercase;
    }
    .hero {
        padding: 2.2rem 2.4rem; margin: 1.1rem 0 1.5rem;
        border: 1px solid rgba(255,255,255,.75); border-radius: 24px;
        background: linear-gradient(120deg, rgba(255,255,255,.96), rgba(230,246,241,.92));
        box-shadow: 0 18px 55px rgba(30, 76, 82, .08);
    }
    .hero h1 { font-size: clamp(2.1rem, 5vw, 3.45rem); line-height: 1.08; margin: .5rem 0; }
    .hero p { max-width: 690px; color: var(--muted); font-size: 1.08rem; margin-bottom: 0; }
    .section-label {
        color: var(--teal); font-size: .76rem; font-weight: 800;
        text-transform: uppercase; letter-spacing: .12em; margin: .3rem 0 .5rem;
    }
    div[data-testid="stForm"] {
        border: 1px solid var(--line); border-radius: 20px;
        background: rgba(255,255,255,.88); padding: 1.45rem 1.6rem;
        box-shadow: 0 10px 36px rgba(28, 70, 73, .055);
    }
    div.stButton > button, div[data-testid="stFormSubmitButton"] button {
        border: 0; border-radius: 12px; color: white;
        background: linear-gradient(135deg, #0b8583, #07646d);
        font-weight: 700; min-height: 2.8rem;
        box-shadow: 0 8px 18px rgba(7, 105, 109, .17);
    }
    div.stButton > button:hover, div[data-testid="stFormSubmitButton"] button:hover {
        color: white; border: 0; filter: brightness(1.06);
    }
    [data-testid="stMetric"] {
        background: white; border: 1px solid var(--line); border-radius: 14px;
        padding: 1rem 1.1rem;
    }
    div[data-testid="stExpander"] {
        border: 1px solid var(--line); border-radius: 14px; background: rgba(255,255,255,.8);
    }
    .small-note { color: var(--muted); font-size: .88rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def _show_itinerary(content: Any) -> None:
    if not content:
        return
    with st.expander("Day-by-day itinerary", expanded=True):
        if isinstance(content, dict):
            days = content.get("days")
            if isinstance(days, list):
                for day in days:
                    if not isinstance(day, dict):
                        st.write(day)
                        continue
                    st.markdown(
                        f"**Day {day.get('day', '')} · {day.get('date', '')}**"
                    )
                    activities = day.get("activities", [])
                    for activity in activities:
                        st.markdown(f"- {activity}")
                    st.divider()
            else:
                st.write(content)
        elif isinstance(content, list):
            for item in content:
                st.write(item)
        else:
            st.write(content)


def _show_transport(content: Any) -> None:
    if not content:
        return
    st.subheader("Getting there")
    options = content.get("options", []) if isinstance(content, dict) else []
    for index, option in enumerate(options, start=1):
        if not isinstance(option, dict):
            st.write(option)
            continue
        title = option.get("mode") or f"Option {index}"
        with st.container(border=True):
            st.markdown(f"**{title}**")
            if option.get("description"):
                st.write(option["description"])
            if option.get("duration"):
                st.caption(f"Estimated duration: {option['duration']}")
            if option.get("cost") is not None:
                st.caption(f"Estimated cost: ₹{option['cost']:,.0f}")
            if option.get("suitability"):
                st.caption(option["suitability"])
    if isinstance(content, dict) and content.get("recommendation"):
        st.info(f"Recommendation: {content['recommendation']}")
    considerations = content.get("considerations", []) if isinstance(content, dict) else []
    for item in considerations:
        st.markdown(f"- {item}")


def _show_hotels(content: Any) -> None:
    if not content:
        return
    st.subheader("Where to stay")
    options = content.get("options", []) if isinstance(content, dict) else []
    for index, option in enumerate(options, start=1):
        if not isinstance(option, dict):
            st.write(option)
            continue
        title = option.get("name") or f"Stay option {index}"
        with st.container(border=True):
            st.markdown(f"**{title}**")
            if option.get("description"):
                st.write(option["description"])
            if option.get("suitability"):
                st.caption(option["suitability"])
            for note in option.get("considerations", []):
                st.markdown(f"- {note}")
    if isinstance(content, dict) and content.get("recommendation"):
        st.info(f"Recommendation: {content['recommendation']}")
    for item in content.get("considerations", []) if isinstance(content, dict) else []:
        st.markdown(f"- {item}")


def _show_validation(content: Any) -> None:
    if not isinstance(content, dict) or "valid" not in content:
        return
    if content["valid"] is True:
        st.success("Plan validation: Valid")
    else:
        st.warning("Plan validation: Not valid")


def _submit_trip(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        response = requests.post(API_URL, json=payload, timeout=(10, 900))
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Could not reach the Travelmate API at {API_URL}. "
            "Check that the FastAPI server is running."
        ) from exc

    if not response.ok:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise RuntimeError(f"Travel planning failed ({response.status_code}): {detail}")

    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError("The Travelmate API returned an invalid response.") from exc
    if not isinstance(result, dict):
        raise RuntimeError("The Travelmate API response had an unexpected format.")
    return result


def _show_trip_form() -> None:
    st.markdown(
        """
        <div class="hero">
          <div class="brand">✈ Travelmate.ai</div>
          <h1>Let’s plan somewhere<br>remarkable.</h1>
          <p>Tell us a little about your trip. Your AI travel team will bring
          together destination ideas, transport, stays, and a day-by-day itinerary.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">01 · Your route</div>', unsafe_allow_html=True)
    with st.form("trip_request"):
        route_from, route_to = st.columns(2)
        with route_from:
            origin = st.text_input(
                "Leaving from",
                placeholder="e.g. Kolkata",
            )
        with route_to:
            destination = st.text_input(
                "Going to",
                placeholder="e.g. Varanasi",
            )

        st.markdown('<div class="section-label">02 · Dates & travellers</div>', unsafe_allow_html=True)
        dates_col, adults_col, children_col = st.columns([2, 1, 1])
        with dates_col:
            date_start, date_end = st.columns(2)
            with date_start:
                start_date = st.date_input(
                    "Start date",
                    value=date.today() + timedelta(days=14),
                    min_value=date.today(),
                )
            with date_end:
                end_date = st.date_input(
                    "End date",
                    value=date.today() + timedelta(days=18),
                    min_value=date.today(),
                )
        with adults_col:
            adults = st.number_input("Adults", min_value=1, value=2, step=1)
        with children_col:
            children = st.number_input("Children", min_value=0, value=0, step=1)

        st.markdown('<div class="section-label">03 · Budget & preferences</div>', unsafe_allow_html=True)
        budget_col, food_col = st.columns([1.2, 1])
        with budget_col:
            budget = st.number_input(
                "Total budget (₹)",
                min_value=0,
                value=60000,
                step=5000,
            )
        with food_col:
            food_preference = st.selectbox(
                "Food preference",
                ["Vegetarian", "Non-vegetarian"],
            )
        preference_text = st.text_area(
            "What would make this trip special?",
            placeholder="For example: temples, relaxed pace, family-friendly activities",
            help="Separate preferences with commas or put each on a new line.",
        )

        submitted = st.form_submit_button(
            "Create my travel plan  →",
            use_container_width=True,
        )

    if submitted:
        if not origin.strip() or not destination.strip():
            st.error("Please enter both your starting point and destination.")
        elif end_date < start_date:
            st.error("The end date must be on or after the start date.")
        else:
            preferences = [
                item.strip()
                for item in preference_text.replace("\n", ",").split(",")
                if item.strip()
            ]
            payload = {
                "origin": origin.strip(),
                "destination": destination.strip(),
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "adults": int(adults),
                "children": int(children),
                "budget": float(budget),
                "preferences": preferences,
                "food_preference": food_preference.lower(),
            }
            try:
                with st.spinner("Your travel team is researching and building your itinerary…"):
                    st.session_state["travel_result"] = _submit_trip(payload)
            except RuntimeError as exc:
                st.error(str(exc))

    result = st.session_state.get("travel_result")
    if not result:
        st.markdown(
            '<p class="small-note">No bookings are made by generating a plan. '
            'Review availability and prices with providers before you travel.</p>',
            unsafe_allow_html=True,
        )
        return

    st.divider()
    st.markdown("## Your trip, thoughtfully planned")
    trip = result.get("trip", {})
    if trip:
        st.caption(
            f"{trip.get('origin', origin if 'origin' in locals() else '')} → "
            f"{trip.get('destination', destination if 'destination' in locals() else '')}"
        )
        metric_cols = st.columns(4)
        metric_cols[0].metric("Dates", f"{trip.get('start_date', '—')} – {trip.get('end_date', '—')}")
        metric_cols[1].metric("Duration", f"{trip.get('trip_duration', '—')} days")
        metric_cols[2].metric(
            "Travellers",
            f"{trip.get('adults', 0)} adults · {trip.get('children', 0)} children",
        )
        metric_cols[3].metric("Budget", f"₹{trip.get('budget', 0):,.0f}")

    _show_itinerary(result.get("itinerary"))
    _show_transport(result.get("transport_options"))
    _show_hotels(result.get("hotel_options"))
    _show_validation(result.get("validation"))


_show_trip_form()