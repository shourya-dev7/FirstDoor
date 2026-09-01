import json
from pathlib import Path
from typing import List, Dict, Any


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_FILE = BASE_DIR / "data" / "hospitals.json"


def load_hospitals() -> List[Dict[str, Any]]:
    """Load the prototype hospital directory."""

    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def find_hospitals(
    specialty: str = "",
    city: str = "",
    emergency: bool = False,
) -> List[Dict[str, Any]]:
    """
    Find hospitals using specialty, city, and emergency availability.

    This is a prototype directory and not a live hospital availability system.
    """

    hospitals = load_hospitals()

    specialty = specialty.strip().lower()
    city = city.strip().lower()

    matches = []

    for hospital in hospitals:

        if city and hospital.get("city", "").lower() != city:
            continue

        if emergency and not hospital.get("emergency_available", False):
            continue

        if specialty:
            hospital_specialties = [
                item.lower()
                for item in hospital.get("specialties", [])
            ]

            if specialty not in hospital_specialties:
                continue

        matches.append(hospital)

    return matches


def get_hospital_referral(
    specialty: str,
    city: str = "Chennai",
    emergency: bool = False,
) -> Dict[str, Any]:
    """
    Generate a structured hospital referral response.
    """

    matches = find_hospitals(
        specialty=specialty,
        city=city,
        emergency=emergency,
    )

    return {
        "specialty_requested": specialty,
        "city": city,
        "emergency": emergency,
        "hospitals": matches,
        "count": len(matches),
        "disclaimer": (
            "This is a prototype hospital directory. "
            "Availability, wait times, and emergency capacity must be "
            "confirmed directly with the healthcare provider."
        ),
    }