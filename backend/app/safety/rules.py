from typing import Any

EMERGENCY_SYMPTOMS = {
    "chest pain",
    "severe chest pain",
    "difficulty breathing",
    "severe difficulty breathing",
    "shortness of breath",
    "loss of consciousness",
    "unconsciousness",
    "seizure",
    "sudden weakness",
    "slurred speech",
    "sudden confusion",
    "severe bleeding",
}


def normalize_answer(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip().lower()

    return str(value).strip().lower()


def find_emergency_symptoms(answers: dict[str, Any]) -> list[str]:
    found: list[str] = []

    for _, value in answers.items():
        text = normalize_answer(value)

        for symptom in EMERGENCY_SYMPTOMS:
            if symptom in text and symptom not in found:
                found.append(symptom)

    return found


def evaluate_safety(answers: dict[str, Any]) -> dict[str, Any]:
    emergency_symptoms = find_emergency_symptoms(answers)

    if emergency_symptoms:
        return {
            "is_emergency": True,
            "risk_band": "emergency",
            "triggers": emergency_symptoms,
        }

    return {
        "is_emergency": False,
        "risk_band": None,
        "triggers": [],
    }