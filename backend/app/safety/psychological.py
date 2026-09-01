from typing import Any


CRISIS_RESPONSE = {
    "risk_band": "crisis",
    "headline": "Immediate crisis support is recommended.",
    "drivers": [],
    "referrals": [],
    "roadmap": [],
    "crisis_support": {
        "name": "Crisis Support",
        "numbers": ["14416", "1800-891-4416"],
    },
}


def is_crisis_answer(answer: Any) -> bool:
    if answer is None:
        return False

    if isinstance(answer, (int, float)):
        return answer != 0

    value = str(answer).strip().lower()

    try:
        numeric_value = float(value)
        return numeric_value != 0
    except ValueError:
        pass

    crisis_values = {
        "yes",
        "y",
        "true",
        "nearly every day",
        "often",
    }

    return value in crisis_values

def find_crisis_item(items: list[dict[str, Any]]) -> dict[str, Any] | None:
    for item in items:
        if item.get("isCrisisItem") is True:
            return item
    return None


def crisis_response() -> dict[str, Any]:
    return {
        "risk_band": "crisis",
        "headline": CRISIS_RESPONSE["headline"],
        "drivers": [],
        "referrals": [],
        "roadmap": [],
        "crisis_support": {
            "name": CRISIS_RESPONSE["crisis_support"]["name"],
            "numbers": list(
                CRISIS_RESPONSE["crisis_support"]["numbers"]
            ),
        },
    }


def run_crisis_gate(
    items: list[dict[str, Any]],
    answers: dict[str, Any],
) -> dict[str, Any] | None:

    crisis_item = find_crisis_item(items)

    # Fail closed if the crisis question is missing.
    if crisis_item is None:
        return crisis_response()

    question_id = crisis_item.get("id")
    answer = answers.get(question_id)

    if is_crisis_answer(answer):
        return crisis_response()

    return None