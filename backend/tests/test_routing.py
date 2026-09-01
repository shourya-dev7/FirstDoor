from app.services.routing_engine import route_specialties


def test_chest_pain_routes_to_cardiology():
    answers = {
        "symptoms": ["chest pain"],
    }

    result = route_specialties(answers)

    assert result
    assert result[0]["specialty"] == "Cardiology"


def test_headache_routes_to_neurology():
    answers = {
        "symptoms": ["headache"],
    }

    result = route_specialties(answers)

    assert result
    assert result[0]["specialty"] == "Neurology"


def test_breathing_problem_routes_to_pulmonology():
    answers = {
        "symptoms": ["difficulty breathing"],
    }

    result = route_specialties(answers)

    assert result
    assert result[0]["specialty"] == "Pulmonology"


def test_unknown_symptom_routes_to_general_medicine():
    answers = {
        "symptoms": ["something unusual"],
    }

    result = route_specialties(answers)

    assert result
    assert result[0]["specialty"] == "General Medicine"