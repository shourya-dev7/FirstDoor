from typing import List, Dict, Any


# Prototype reference ranges for demonstration.
# Real clinical use requires lab-specific ranges, units, age, sex, and clinical context.
LAB_RANGES = {
    "hemoglobin": {
        "min": 12.0,
        "max": 17.5,
        "unit": "g/dL",
    },
    "glucose_fasting": {
        "min": 70,
        "max": 99,
        "unit": "mg/dL",
    },
    "total_cholesterol": {
        "min": 0,
        "max": 200,
        "unit": "mg/dL",
    },
    "creatinine": {
        "min": 0.6,
        "max": 1.3,
        "unit": "mg/dL",
    },
    "wbc": {
        "min": 4000,
        "max": 11000,
        "unit": "cells/uL",
    },
    "platelets": {
        "min": 150000,
        "max": 450000,
        "unit": "cells/uL",
    },
}


def analyze_labs(labs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Prototype laboratory analysis.

    Input example:
    [
        {"test": "hemoglobin", "value": 10.5},
        {"test": "glucose_fasting", "value": 130}
    ]
    """

    results = []
    abnormalities = []

    for lab in labs:
        test = str(lab.get("test", "")).lower().strip()
        value = lab.get("value")

        if test not in LAB_RANGES:
            results.append({
                "test": test,
                "value": value,
                "status": "unknown_reference_range",
                "message": "No prototype reference range is configured for this test."
            })
            continue

        if value is None:
            results.append({
                "test": test,
                "value": value,
                "status": "invalid",
                "message": "A numeric value is required."
            })
            continue

        try:
            value = float(value)
        except (TypeError, ValueError):
            results.append({
                "test": test,
                "value": value,
                "status": "invalid",
                "message": "Lab value must be numeric."
            })
            continue

        reference = LAB_RANGES[test]

        if value < reference["min"]:
            status = "low"
        elif value > reference["max"]:
            status = "high"
        else:
            status = "normal"

        result = {
            "test": test,
            "value": value,
            "unit": reference["unit"],
            "status": status,
            "reference_range": {
                "min": reference["min"],
                "max": reference["max"],
            },
        }

        results.append(result)

        if status in ["low", "high"]:
            abnormalities.append(result)

    risk_contribution = "low"

    if len(abnormalities) >= 3:
        risk_contribution = "high"
    elif len(abnormalities) >= 1:
        risk_contribution = "moderate"

    return {
        "results": results,
        "abnormalities": abnormalities,
        "risk_contribution": risk_contribution,
        "requires_clinician_review": True,
        "disclaimer": (
            "This prototype provides decision-support only and does not "
            "diagnose disease. Laboratory interpretation requires clinical context."
        ),
    }