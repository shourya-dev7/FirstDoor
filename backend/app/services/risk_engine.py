from typing import Any


def calculate_risk(
    answers: dict[str, Any],
    safety_result: dict[str, Any],
) -> dict[str, Any]:

    # Emergency cases must never receive a normal risk score.
    if safety_result.get("is_emergency"):
        return {
            "risk_band": "emergency",
            "risk_score": None,
            "drivers": [],
        }

    score = 0
    drivers: list[dict[str, str]] = []

    # Severity
    severity = answers.get("severity")

    try:
        severity_value = int(severity)
    except (TypeError, ValueError):
        severity_value = 0

    if severity_value >= 8:
        score += 30
        drivers.append({
            "question_id": "severity",
            "answer": str(severity),
        })

    elif severity_value >= 5:
        score += 15
        drivers.append({
            "question_id": "severity",
            "answer": str(severity),
        })

    # Symptoms
    symptoms = answers.get("symptoms", [])

    if isinstance(symptoms, str):
        symptoms = [symptoms]

    if isinstance(symptoms, list):
        for symptom in symptoms:
            text = str(symptom).lower()

            if "chest pain" in text:
                score += 25
                drivers.append({
                    "question_id": "symptom",
                    "answer": str(symptom),
                })

            elif "difficulty breathing" in text:
                score += 25
                drivers.append({
                    "question_id": "symptom",
                    "answer": str(symptom),
                })

            elif symptom:
                score += 5
                drivers.append({
                    "question_id": "symptom",
                    "answer": str(symptom),
                })

    # Medical history
    history = answers.get("medical_history", [])

    if isinstance(history, str):
        history = [history]

    if isinstance(history, list):
        for item in history:
            text = str(item).lower()

            important_conditions = [
                "heart disease",
                "hypertension",
                "high blood pressure",
                "diabetes",
                "previous stroke",
            ]

            if any(
                condition in text
                for condition in important_conditions
            ):
                score += 10
                drivers.append({
                    "question_id": "medical_history",
                    "answer": str(item),
                })

    # Keep score within 0–100.
    score = min(score, 100)

    # Convert score into the contract's risk bands.
    if score >= 70:
        band = "urgent"
    elif score >= 45:
        band = "soon"
    else:
        band = "routine"

    return {
        "risk_band": band,
        "risk_score": score,
        "drivers": drivers,
    }