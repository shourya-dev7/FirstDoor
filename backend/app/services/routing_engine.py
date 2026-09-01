from typing import Any


SPECIALTY_RULES = {
    "Cardiology": [
        "chest pain",
        "palpitations",
        "heart",
        "high blood pressure",
    ],
    "Neurology": [
        "headache",
        "seizure",
        "sudden weakness",
        "slurred speech",
        "numbness",
    ],
    "Pulmonology": [
        "difficulty breathing",
        "shortness of breath",
        "persistent cough",
        "wheezing",
    ],
    "Endocrinology": [
        "diabetes",
        "excessive thirst",
        "frequent urination",
    ],
    "Gastroenterology": [
        "abdominal pain",
        "stomach pain",
        "vomiting",
        "diarrhea",
    ],
    "Nephrology": [
        "kidney",
        "blood in urine",
        "swelling",
    ],
    "Dermatology": [
        "rash",
        "skin",
        "itching",
    ],
    "Orthopaedics": [
        "joint pain",
        "bone pain",
        "back pain",
    ],
    "ENT": [
        "ear pain",
        "hearing",
        "sinus",
        "sore throat",
    ],
    "Ophthalmology": [
        "vision",
        "eye pain",
        "blurred vision",
    ],
    "Psychiatry": [
        "depression",
        "anxiety",
        "panic",
    ],
    "General Medicine": [],
}


def _collect_text(answers: dict[str, Any]) -> str:
    values: list[str] = []

    for value in answers.values():
        if isinstance(value, list):
            values.extend(str(v) for v in value)
        else:
            values.append(str(value))

    return " ".join(values).lower()


def route_specialties(
    answers: dict[str, Any],
) -> list[dict[str, Any]]:

    text = _collect_text(answers)

    scored: list[dict[str, Any]] = []

    for specialty, keywords in SPECIALTY_RULES.items():

        if specialty == "General Medicine":
            continue

        matches = [
            keyword
            for keyword in keywords
            if keyword in text
        ]

        if matches:
            scored.append({
                "specialty": specialty,
                "score": len(matches),
                "matches": matches,
            })

    scored.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    referrals: list[dict[str, Any]] = []

    for index, item in enumerate(scored, start=1):
        matches = ", ".join(item["matches"])

        referrals.append({
            "specialty": item["specialty"],
            "rank": index,
            "rationale": (
                f"Relevant reported factors: {matches}."
            ),
        })

    if not referrals:
        referrals.append({
            "specialty": "General Medicine",
            "rank": 1,
            "rationale": (
                "General medical evaluation is appropriate "
                "when no specific specialty pathway is strongly matched."
            ),
        })

    return referrals