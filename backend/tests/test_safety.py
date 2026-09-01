from app.safety.psychological import run_crisis_gate


def test_crisis_gate_detects_crisis_before_scoring():
    items = [
        {"id": "phq9-1"},
        {"id": "phq9-9", "isCrisisItem": True},
    ]

    answers = {
        "phq9-9": 1,
        "severity": 10,
    }

    result = run_crisis_gate(items, answers)

    assert result is not None
    assert result["risk_band"] == "crisis"
    assert result["drivers"] == []
    assert result["referrals"] == []
    assert result["roadmap"] == []
    assert result["crisis_support"] is not None


def test_crisis_gate_is_not_triggered_by_zero():
    items = [
        {"id": "phq9-9", "isCrisisItem": True},
    ]

    answers = {
        "phq9-9": 0,
    }

    result = run_crisis_gate(items, answers)

    assert result is None


def test_missing_crisis_item_fails_closed():
    items = [
        {"id": "phq9-1"},
        {"id": "phq9-2"},
    ]

    answers = {
        "phq9-1": 0,
        "phq9-2": 0,
    }

    result = run_crisis_gate(items, answers)

    assert result is not None
    assert result["risk_band"] == "crisis"