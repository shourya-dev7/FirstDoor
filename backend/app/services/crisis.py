"""
FirstDoor Crisis Safety Service

CRITICAL SAFETY RULE:
Crisis detection happens BEFORE any psychological scoring.

This module:
1. Looks for the crisis/self-harm question by its FLAG.
2. Never assumes the crisis question is at a particular index.
3. Fails closed if the crisis item cannot be found.
4. Returns immediately when crisis risk is detected.
5. Does not calculate a PHQ-9/GAD-7 score.
"""

from typing import Any, Dict, List, Optional


# -------------------------------------------------------------------
# Crisis result
# -------------------------------------------------------------------

CRISIS_RESULT = {
    "risk_band": "crisis",
    "headline": "Immediate support is recommended.",
    "drivers": [],
    "referrals": [],
    "roadmap": [],
    "crisis_support": {
        "name": "Emergency and Crisis Support",
        "numbers": [
            "112"
        ],
    },
}


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def _normalise(value: Any) -> str:
    """
    Convert an answer into a predictable lowercase string.
    """
    if value is None:
        return ""

    if isinstance(value, bool):
        return "yes" if value else "no"

    return str(value).strip().lower()


def _is_crisis_answer(answer: Any) -> bool:
    """
    Determine whether an answer indicates self-harm/suicide risk.

    We deliberately keep this deterministic.
    The LLM is NOT involved in this decision.
    """

    value = _normalise(answer)

    crisis_values = {
        "yes",
        "y",
        "true",
        "1",
        "often",
        "nearly every day",
        "several days",
        "more than half the days",
        "i have",
        "i do",
        "i am",
        "present",
        "positive",
    }

    return value in crisis_values


# -------------------------------------------------------------------
# Find the crisis item by FLAG
# -------------------------------------------------------------------

def find_crisis_item(
    questions: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Find the crisis question using its explicit flag.

    IMPORTANT:
    We do NOT use an array index.

    Therefore questions can be reordered without breaking
    the crisis safety gate.
    """

    for question in questions:
        if question.get("crisis") is True:
            return question

        if question.get("is_crisis") is True:
            return question

        if question.get("crisis_flag") is True:
            return question

        flags = question.get("flags", [])

        if isinstance(flags, list) and "crisis" in flags:
            return question

    return None


# -------------------------------------------------------------------
# Main crisis gate
# -------------------------------------------------------------------

def check_crisis(
    questions: List[Dict[str, Any]],
    answers: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Execute the crisis gate.

    SAFETY GUARANTEE:

        crisis check
             ↓
        crisis found?
          /       \
        YES       NO
         ↓         ↓
      STOP      scoring

    If the crisis question cannot be found, we FAIL CLOSED.

    That means we return a crisis result instead of silently
    continuing with scoring.
    """

    # ---------------------------------------------------------------
    # STEP 1 — Find crisis item by FLAG
    # ---------------------------------------------------------------

    crisis_item = find_crisis_item(questions)

    # ---------------------------------------------------------------
    # STEP 2 — FAIL CLOSED
    # ---------------------------------------------------------------

    if crisis_item is None:
        return dict(CRISIS_RESULT)

    # ---------------------------------------------------------------
    # STEP 3 — Get the question ID
    # ---------------------------------------------------------------

    question_id = crisis_item.get("id")

    if not question_id:
        # No identifiable crisis question = unsafe configuration.
        # Fail closed.
        return dict(CRISIS_RESULT)

    # ---------------------------------------------------------------
    # STEP 4 — Get the user's answer
    # ---------------------------------------------------------------

    answer = answers.get(question_id)

    # ---------------------------------------------------------------
    # STEP 5 — Crisis detected
    # ---------------------------------------------------------------

    if _is_crisis_answer(answer):
        return dict(CRISIS_RESULT)

    # ---------------------------------------------------------------
    # STEP 6 — No crisis
    # ---------------------------------------------------------------

    return {
        "risk_band": None,
        "headline": "",
        "drivers": [],
        "referrals": [],
        "roadmap": [],
        "crisis_support": None,
    }