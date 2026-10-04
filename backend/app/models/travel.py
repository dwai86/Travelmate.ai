from typing import List, Optional

from pydantic import BaseModel, Field


class TravelRequest(BaseModel):
    """Structured information extracted from the user's travel request."""

    origin: Optional[str] = Field(
        default=None,
        description="City or place from which the user will start the trip"
    )

    destination: Optional[str] = Field(
        default=None,
        description="Primary travel destination"
    )

    start_date: Optional[str] = Field(
        default=None,
        description="Trip start date in YYYY-MM-DD format"
    )

    end_date: Optional[str] = Field(
        default=None,
        description="Trip end date in YYYY-MM-DD format"
    )

    trip_duration: Optional[int] = Field(
    default=None,
    description="Number of days for the trip"
    )

    adults: Optional[int] = Field(
        default=None,
        description="Number of adult travelers"
    )

    children: Optional[int] = Field(
        default=None,
        description="Number of child travelers"
    )

    budget: Optional[float] = Field(
        default=None,
        description="Maximum total trip budget"
    )

    preferences: List[str] = Field(
        default_factory=list,
        description="Travel preferences and constraints mentioned by the user"
    )

class Place(BaseModel):
    name: str
    category: str
    description: str
    relevance: str


class DestinationResearch(BaseModel):
    places: List[Place]
    activities: List[str]
    travel_tips: List[str]
    preference_matches: List[str]


class TransportOption(BaseModel):
    mode: str
    description: str
    duration: Optional[str] = None
    suitability: str


class TransportResearch(BaseModel):
    options: List[TransportOption]
    recommendation: str
    considerations: List[str]


class ItineraryDay(BaseModel):
    day: int
    date: str
    activities: List[str]


class Itinerary(BaseModel):
    days: List[ItineraryDay]


class ValidationResult(BaseModel):
    valid: bool
    issues: List[str]
    recommendations: List[str]

class HotelOption(BaseModel):
    name: str
    description: str
    suitability: str
    considerations: List[str]


class HotelResearch(BaseModel):
    options: List[HotelOption]
    recommendation: str
    considerations: List[str]