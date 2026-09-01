from app.services.decision_engine import run_decision_engine


def test_normal_case_returns_valid_triage_response():
    answers = {
        "severity": 6,
        "symptoms": ["headache"],
        "medical_history": [],
    }

    result = run_decision_engine(
        answers=answers,
        instrument=None,
    )

    assert result["risk_band"] in {"routine", "soon", "urgent"}
    assert isinstance(result["drivers"], list)
    assert isinstance(result["referrals"], list)
    assert isinstance(result["roadmap"], list)
    assert result["crisis_support"] is None


def test_emergency_case_stops_normal_decision_flow():
    answers = {
        "severity": 10,
        "symptoms": ["chest pain"],
        "medical_history": [],
    }

    result = run_decision_engine(
        answers=answers,
        instrument=None,
    )

    assert result["risk_band"] == "emergency"
    assert result["referrals"] == []
    assert result["roadmap"] == []
    assert result["crisis_support"] is None


def test_phq9_crisis_case_returns_crisis_response():
    psychological_items = [
        {"id": "phq9-1"},
        {"id": "phq9-9", "isCrisisItem": True},
    ]

    answers = {
        "phq9-9": 1,
        "severity": 10,
        "symptoms": ["chest pain"],
    }

    result = run_decision_engine(
        answers=answers,
        instrument="phq9",
        psychological_items=psychological_items,
    )

    assert result["risk_band"] == "crisis"
    assert result["drivers"] == []
    assert result["referrals"] == []
    assert result["roadmap"] == []
    assert result["crisis_support"] is not None


def test_phq9_missing_crisis_item_fails_closed():
    psychological_items = [
        {"id": "phq9-1"},
        {"id": "phq9-2"},
    ]

    answers = {
        "phq9-1": 0,
        "phq9-2": 0,
    }

    result = run_decision_engine(
        answers=answers,
        instrument="phq9",
        psychological_items=psychological_items,
    )

    assert result["risk_band"] == "crisis"