from typing import Any

from app.safety.rules import evaluate_safety
from app.safety.psychological import run_crisis_gate
from app.services.risk_engine import calculate_risk
from app.services.routing_engine import route_specialties


def build_headline(risk_band: str) -> str:
    headlines = {
        "crisis": "Immediate crisis support is recommended.",
        "emergency": "Emergency medical evaluation is recommended.",
        "urgent": "Your symptoms warrant prompt clinical evaluation.",
        "soon": "A clinical evaluation should be arranged soon.",
        "routine": "Routine clinical follow-up may be appropriate.",
    }

    return headlines.get(
        risk_band,
        "Clinical evaluation is recommended.",
    )


def build_roadmap(
    risk_band: str,
) -> list[dict[str, Any]]:

    if risk_band == "crisis":
        return []

    if risk_band == "emergency":
        return []

    if risk_band == "urgent":
        return [
            {
                "stage": "Now",
                "actions": [
                    "Arrange prompt medical evaluation."
                ],
            },
            {
                "stage": "Consultation",
                "actions": [
                    "Discuss symptoms and medical history with a clinician."
                ],
            },
            {
                "stage": "Follow-up",
                "actions": [
                    "Follow the clinician's recommended plan."
                ],
            },
        ]

    if risk_band == "soon":
        return [
            {
                "stage": "Within 48 hours",
                "actions": [
                    "Arrange an appropriate clinical consultation."
                ],
            },
            {
                "stage": "Consultation",
                "actions": [
                    "Discuss relevant investigations with the clinician."
                ],
            },
            {
                "stage": "Follow-up",
                "actions": [
                    "Follow the clinician's recommended review."
                ],
            },
        ]

    return [
        {
            "stage": "Routine",
            "actions": [
                "Monitor symptoms and consider routine medical follow-up."
            ],
        },
        {
            "stage": "Follow-up",
            "actions": [
                "Seek further evaluation if symptoms persist or worsen."
            ],
        },
    ]


def validate_triage_response(response: dict) -> dict:

    assert response["risk_band"] in {
        "crisis",
        "emergency",
        "urgent",
        "soon",
        "routine",
    }

    assert isinstance(response["headline"], str)
    assert isinstance(response["drivers"], list)
    assert isinstance(response["referrals"], list)
    assert isinstance(response["roadmap"], list)

    for driver in response["drivers"]:
        assert isinstance(driver, dict)
        assert isinstance(driver["question_id"], str)
        assert isinstance(driver["answer"], str)

    for referral in response["referrals"]:
        assert isinstance(referral, dict)
        assert isinstance(referral["specialty"], str)
        assert isinstance(referral["rank"], int)
        assert isinstance(referral["rationale"], str)

    for stage in response["roadmap"]:
        assert isinstance(stage, dict)
        assert isinstance(stage["stage"], str)
        assert isinstance(stage["actions"], list)

        for action in stage["actions"]:
            assert isinstance(action, str)

    if response["risk_band"] == "crisis":
        assert response["drivers"] == []
        assert response["referrals"] == []
        assert response["roadmap"] == []

        assert response["crisis_support"] is not None
        assert isinstance(
            response["crisis_support"]["name"],
            str,
        )
        assert isinstance(
            response["crisis_support"]["numbers"],
            list,
        )

        for number in response["crisis_support"]["numbers"]:
            assert isinstance(number, str)

    else:
        assert response["crisis_support"] is None

    if response["risk_band"] == "emergency":
        assert response["referrals"] == []
        assert response["roadmap"] == []

    return response


def run_decision_engine(
    answers: dict[str, Any],
    instrument: str | None,
    psychological_items: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:

    psychological_items = psychological_items or []

    # 1. CRISIS GATE — must happen before scoring.
    if instrument == "phq9":
        crisis_result = run_crisis_gate(psychological_items, answers)
        if crisis_result is not None:
            return crisis_result

    # 2. GENERAL EMERGENCY SAFETY GATE.
    safety_result = evaluate_safety(answers)

    if safety_result["is_emergency"]:

        drivers = [
            {
                "question_id": "safety",
                "answer": trigger,
            }
            for trigger in safety_result["triggers"]
        ]

        return validate_triage_response({
            "risk_band": "emergency",
            "headline": build_headline("emergency"),
            "drivers": drivers,
            "referrals": [],
            "roadmap": [],
            "crisis_support": None,
        })

    # 3. ONLY NOW calculate normal risk.
    risk_result = calculate_risk(
        answers,
        safety_result,
    )

    risk_band = risk_result["risk_band"]

    # 4. SPECIALTY ROUTING.
    referrals = route_specialties(answers)

    # 5. ROADMAP.
    roadmap = build_roadmap(risk_band)

    # 6. Build the exact frontend contract.
    return validate_triage_response({
        "risk_band": risk_band,
        "headline": build_headline(risk_band),
        "drivers": risk_result["drivers"],
        "referrals": referrals,
        "roadmap": roadmap,
        "crisis_support": None,
    })