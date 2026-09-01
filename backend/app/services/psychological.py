"""
FirstDoor Psychological Screening Service

Supports:
- PHQ-9
- GAD-7
- Crisis-first safety gate

IMPORTANT ARCHITECTURAL RULE:

The crisis check MUST happen before any psychological scoring.

The crisis question is located using a `crisis_flag`, NOT by
assuming a particular question index.

If no question contains the crisis flag, the system FAILS CLOSED
and returns a crisis result rather than silently scoring the patient.
"""

from typing import Any, Dict, List, Optional


# ============================================================
# PHQ-9
# ============================================================

PHQ9_QUESTIONS = [
    {
        "id": "phq9_1",
        "text": "Little interest or pleasure in doing things?",
        "crisis_flag": False,
    },
    {
        "id": "phq9_2",
        "text": "Feeling down, depressed, or hopeless?",
        "crisis_flag": False,
    },
    {
        "id": "phq9_3",
        "text": "Trouble falling or staying asleep, or sleeping too much?",
        "crisis_flag": False,
    },
    {
        "id": "phq9_4",
        "text": "Feeling tired or having little energy?",
        "crisis_flag": False,
    },
    {
        "id": "phq9_5",
        "text": "Poor appetite or overeating?",
        "crisis_flag": False,
    },
    {
        "id": "phq9_6",
        "text": "Feeling bad about yourself — or that you are a failure or have let yourself or your family down?",
        "crisis_flag": False,
    },
    {
        "id": "phq9_7",
        "text": "Trouble concentrating on things, such as reading the newspaper or watching television?",
        "crisis_flag": False,
    },
    {
        "id": "phq9_8",
        "text": "Moving or speaking so slowly that other people could have noticed? Or being so fidgety or restless that you have been moving around a lot more than usual?",
        "crisis_flag": False,
    },
    {
        "id": "phq9_9",
        "text": "Thoughts that you would be better off dead or of hurting yourself?",
        "crisis_flag": True,
    },
]


# ============================================================
# GAD-7
# ============================================================

GAD7_QUESTIONS = [
    {
        "id": "gad7_1",
        "text": "Feeling nervous, anxious, or on edge?",
        "crisis_flag": False,
    },
    {
        "id": "gad7_2",
        "text": "Not being able to stop or control worrying?",
        "crisis_flag": False,
    },
    {
        "id": "gad7_3",
        "text": "Worrying too much about different things?",
        "crisis_flag": False,
    },
    {
        "id": "gad7_4",
        "text": "Trouble relaxing?",
        "crisis_flag": False,
    },
    {
        "id": "gad7_5",
        "text": "Being so restless that it is hard to sit still?",
        "crisis_flag": False,
    },
    {
        "id": "gad7_6",
        "text": "Becoming easily annoyed or irritable?",
        "crisis_flag": False,
    },
    {
        "id": "gad7_7",
        "text": "Feeling afraid as if something awful might happen?",
        "crisis_flag": False,
    },
]


# ============================================================
# Response scoring
# ============================================================

ANSWER_SCORES = {
    "not at all": 0,
    "several days": 1,
    "more than half the days": 2,
    "nearly every day": 3,
}


def normalize_answer(answer: Any) -> str:
    """
    Convert an answer to a normalized string.

    This allows the frontend to send values with different
    capitalization or surrounding whitespace.
    """

    if answer is None:
        return ""

    return str(answer).strip().lower()


def score_answer(answer: Any) -> int:
    """
    Convert a PHQ-9/GAD-7 answer into its numeric score.

    Unknown answers safely receive 0 rather than crashing
    the backend.
    """

    normalized = normalize_answer(answer)

    return ANSWER_SCORES.get(normalized, 0)


# ============================================================
# Crisis gate
# ============================================================

def find_crisis_question(
    questions: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Find the crisis question using the crisis_flag.

    IMPORTANT:
    We deliberately do NOT use an index such as questions[8].

    This means the question list can be reordered without
    disconnecting the safety gate.
    """

    for question in questions:
        if question.get("crisis_flag") is True:
            return question

    return None


def crisis_gate(
    answers: Dict[str, Any],
    questions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Run the crisis check BEFORE any scoring.

    If the crisis question cannot be found, fail closed.

    Returns:
        {
            "is_crisis": bool,
            "question_id": str | None,
            "answer": str | None,
            "reason": str
        }
    """

    crisis_question = find_crisis_question(questions)

    # --------------------------------------------------------
    # FAIL CLOSED
    # --------------------------------------------------------

    if crisis_question is None:
        return {
            "is_crisis": True,
            "question_id": None,
            "answer": None,
            "reason": "Crisis question is missing. Safety gate failed closed.",
        }

    question_id = crisis_question["id"]

    answer = answers.get(question_id)

    normalized = normalize_answer(answer)

    # --------------------------------------------------------
    # Crisis responses
    # --------------------------------------------------------

    crisis_answers = {
        "more than half the days",
        "nearly every day",
        "yes",
        "yes, recently",
        "yes recently",
        "yes, i have",
        "yes i have",
    }

    if normalized in crisis_answers:
        return {
            "is_crisis": True,
            "question_id": question_id,
            "answer": str(answer),
            "reason": "Positive response to crisis screening question.",
        }

    # --------------------------------------------------------
    # No crisis detected
    # --------------------------------------------------------

    return {
        "is_crisis": False,
        "question_id": question_id,
        "answer": str(answer) if answer is not None else None,
        "reason": "No crisis response detected.",
    }


# ============================================================
# PHQ-9 / GAD-7 scoring
# ============================================================

def calculate_score(
    answers: Dict[str, Any],
    questions: List[Dict[str, Any]],
) -> int:
    """
    Calculate the screening score.

    This function should ONLY be called AFTER crisis_gate()
    has passed.
    """

    total = 0

    for question in questions:
        question_id = question["id"]

        # Never score the crisis item here.
        if question.get("crisis_flag") is True:
            continue

        total += score_answer(answers.get(question_id))

    return total


def phq9_severity(score: int) -> str:
    """
    Interpret PHQ-9 score for screening purposes.

    This is not a diagnosis.
    """

    if score <= 4:
        return "minimal"
    elif score <= 9:
        return "mild"
    elif score <= 14:
        return "moderate"
    elif score <= 19:
        return "moderately_severe"
    else:
        return "severe"


def gad7_severity(score: int) -> str:
    """
    Interpret GAD-7 score for screening purposes.

    This is not a diagnosis.
    """

    if score <= 4:
        return "minimal"
    elif score <= 9:
        return "mild"
    elif score <= 14:
        return "moderate"
    else:
        return "severe"


# ============================================================
# Main psychological screening function
# ============================================================

def run_psychological_screening(
    answers: Dict[str, Any],
    instrument: Optional[str],
) -> Dict[str, Any]:
    """
    Main entry point for psychological screening.

    Supported instruments:
        - phq9
        - gad7
        - None

    CRITICAL ORDER:

        1. Select screening questions
        2. Run crisis gate
        3. If crisis -> STOP
        4. Only then calculate score
        5. Return screening result
    """

    # --------------------------------------------------------
    # No psychological screening selected
    # --------------------------------------------------------

    if instrument is None:
        return {
            "instrument": None,
            "is_crisis": False,
            "score": None,
            "severity": None,
            "crisis_question_id": None,
            "crisis_answer": None,
            "reason": "No psychological screening instrument selected.",
        }

    # --------------------------------------------------------
    # Select instrument
    # --------------------------------------------------------

    instrument = instrument.lower().strip()

    if instrument == "phq9":
        questions = PHQ9_QUESTIONS

    elif instrument == "gad7":
        questions = GAD7_QUESTIONS

    else:
        raise ValueError(
            "Unsupported psychological instrument. "
            "Use 'phq9', 'gad7', or null."
        )

    # --------------------------------------------------------
    # STEP 1 — CRISIS GATE
    #
    # This MUST happen before scoring.
    # --------------------------------------------------------

    crisis_result = crisis_gate(
        answers=answers,
        questions=questions,
    )

    # --------------------------------------------------------
    # STEP 2 — CRISIS DETECTED
    #
    # STOP. DO NOT SCORE.
    # --------------------------------------------------------

    if crisis_result["is_crisis"]:
        return {
            "instrument": instrument,
            "is_crisis": True,
            "score": None,
            "severity": None,
            "crisis_question_id": crisis_result["question_id"],
            "crisis_answer": crisis_result["answer"],
            "reason": crisis_result["reason"],
        }

    # --------------------------------------------------------
    # STEP 3 — SAFE TO SCORE
    # --------------------------------------------------------

    score = calculate_score(
        answers=answers,
        questions=questions,
    )

    # --------------------------------------------------------
    # STEP 4 — Severity
    # --------------------------------------------------------

    if instrument == "phq9":
        severity = phq9_severity(score)
    else:
        severity = gad7_severity(score)

    # --------------------------------------------------------
    # STEP 5 — Final result
    # --------------------------------------------------------

    return {
        "instrument": instrument,
        "is_crisis": False,
        "score": score,
        "severity": severity,
        "crisis_question_id": crisis_result["question_id"],
        "crisis_answer": crisis_result["answer"],
        "reason": crisis_result["reason"],
    }


# ============================================================
# Utility function for frontend/backend integration
# ============================================================

def get_questions(instrument: str) -> List[Dict[str, Any]]:
    """
    Return the questions for the requested screening instrument.
    """

    instrument = instrument.lower().strip()

    if instrument == "phq9":
        return PHQ9_QUESTIONS.copy()

    if instrument == "gad7":
        return GAD7_QUESTIONS.copy()

    raise ValueError(
        "Unsupported psychological instrument. "
        "Use 'phq9' or 'gad7'."
    )