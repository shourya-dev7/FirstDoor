from typing import Dict, Any, List


SUPPORTED_MODALITIES = [
    "xray",
    "ct",
    "mri",
    "ultrasound",
    "other",
]


def analyze_imaging(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prototype imaging decision-support module.

    This module does NOT diagnose disease from medical images.
    It accepts structured imaging information and returns a
    decision-support summary for the FirstDoor prototype.
    """

    modality = str(data.get("modality", "")).strip().lower()
    body_part = str(data.get("body_part", "")).strip()
    findings = str(data.get("findings", "")).strip()
    urgency = str(data.get("urgency", "")).strip().lower()

    warnings: List[str] = []

    if modality not in SUPPORTED_MODALITIES:
        warnings.append(
            "Unknown imaging modality. The result should be reviewed by a clinician."
        )

    if not modality:
        warnings.append("Imaging modality was not provided.")

    if not body_part:
        warnings.append("Body part or anatomical region was not provided.")

    if not findings:
        warnings.append(
            "No structured imaging findings were provided. Automated image diagnosis is not enabled in this prototype."
        )

    risk_contribution = "low"

    urgent_keywords = [
    "fracture",
    "bleeding",
    "hemorrhage",
    "stroke",
    "mass effect",
    "pneumothorax",
    "embolism",
    "rupture",
    ]

    text_to_check = findings.lower()

    if any(keyword in text_to_check for keyword in urgent_keywords):
        risk_contribution = "high"

    elif findings:
        risk_contribution = "moderate"

    if urgency in ["emergency", "critical"]:
        risk_contribution = "high"

    requires_clinician_review = True

    return {
        "modality": modality or None,
        "body_part": body_part or None,
        "findings": findings or None,
        "risk_contribution": risk_contribution,
        "requires_clinician_review": requires_clinician_review,
        "warnings": warnings,
        "ai_image_analysis": False,
        "disclaimer": (
            "This prototype provides clinical decision-support only and does not "
            "diagnose disease. Medical imaging must be interpreted by qualified "
            "radiology and healthcare professionals."
        ),
    }