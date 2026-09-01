from app.safety.psychological import is_crisis_answer


def test_zero_is_not_crisis():
    assert is_crisis_answer(0) is False


def test_nonzero_numeric_is_crisis():
    assert is_crisis_answer(1) is True
    assert is_crisis_answer(2) is True
    assert is_crisis_answer(3) is True


def test_numeric_string_is_handled():
    assert is_crisis_answer("0") is False
    assert is_crisis_answer("2") is True


def test_text_crisis_answers_are_detected():
    assert is_crisis_answer("yes") is True
    assert is_crisis_answer("true") is True