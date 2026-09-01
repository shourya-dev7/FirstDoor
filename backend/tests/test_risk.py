from app.services.risk_engine import calculate_risk


def test_low_risk_is_routine():
    answers = {
        "severity": 2,
        "symptoms": ["mild headache"],
        "medical_history": [],
    }

    safety_result = {
        "is_emergency": False,
    }

    result = calculate_risk(answers, safety_result)

    assert result["risk_band"] == "routine"
    assert result["risk_score"] is not None


def test_high_severity_increases_risk():
    answers = {
        "severity": 9,
        "symptoms": [],
        "medical_history": [],
    }

    safety_result = {
        "is_emergency": False,
    }

    result = calculate_risk(answers, safety_result)

    assert result["risk_band"] == "routine"
    assert result["risk_score"] == 30


def test_emergency_does_not_get_normal_risk_score():
    answers = {
        "severity": 10,
        "symptoms": ["chest pain"],
        "medical_history": [],
    }

    safety_result = {
        "is_emergency": True,
    }

    result = calculate_risk(answers, safety_result)

    assert result["risk_band"] == "emergency"
    assert result["risk_score"] is None