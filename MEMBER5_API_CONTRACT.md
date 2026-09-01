# FirstDoor Member 5 API Integration Contract

This document defines the API contract for the Member 5 modules.

The backend should integrate these modules without changing their existing function behavior.

---

# 1. Laboratory Analysis

## Endpoint

POST /labs/analyze

## Request

```json
{
  "labs": [
    {
      "test": "hemoglobin",
      "value": 10.5
    },
    {
      "test": "glucose_fasting",
      "value": 130
    },
    {
      "test": "wbc",
      "value": 7000
    }
  ]
}
```

## Backend Integration

```python
from labs import analyze_labs

result = analyze_labs(labs)
```

## Expected Response

```json
{
  "results": [
    {
      "test": "hemoglobin",
      "value": 10.5,
      "unit": "g/dL",
      "status": "low",
      "reference_range": {
        "min": 12.0,
        "max": 17.5
      }
    }
  ],
  "abnormalities": [],
  "risk_contribution": "moderate",
  "requires_clinician_review": true,
  "disclaimer": "This prototype provides decision-support only and does not diagnose disease. Laboratory interpretation requires clinical context."
}
```

---

# 2. Imaging Analysis

## Endpoint

POST /imaging/analyze

## Request

```json
{
  "modality": "xray",
  "body_part": "chest",
  "findings": "Structured finding available for clinician review"
}
```

## Backend Integration

```python
from imaging import analyze_imaging

result = analyze_imaging(data)
```

## Expected Response

```json
{
  "modality": "xray",
  "body_part": "chest",
  "findings": "Structured finding available for clinician review",
  "risk_contribution": "moderate",
  "requires_clinician_review": true,
  "warnings": [],
  "ai_image_analysis": false,
  "disclaimer": "This prototype provides clinical decision-support only and does not diagnose disease. Medical imaging must be interpreted by qualified radiology and healthcare professionals."
}
```

## Important Imaging Rule

- This module currently accepts structured imaging information.
- `ai_image_analysis` remains `false`.
- It does not perform autonomous radiological diagnosis.
- All imaging results require clinician/radiologist review.

---

# 3. Hospital Referral

## Endpoint

POST /hospitals/referral

## Request

```json
{
  "specialty": "Cardiology",
  "city": "Chennai",
  "emergency": false
}
```

## Backend Integration

```python
from hospitals import get_hospital_referral

result = get_hospital_referral(
    specialty=specialty,
    city=city,
    emergency=emergency
)
```

## Expected Response

```json
{
  "specialty_requested": "Cardiology",
  "city": "Chennai",
  "emergency": false,
  "hospitals": [
    {
      "id": "hospital_001",
      "name": "City General Hospital",
      "city": "Chennai",
      "specialties": [
        "General Medicine",
        "Cardiology",
        "Neurology",
        "Emergency Medicine"
      ],
      "emergency_available": true
    }
  ],
  "count": 1,
  "disclaimer": "This is a prototype hospital directory. Availability, wait times, and emergency capacity must be confirmed directly with the healthcare provider."
}
```

---

# 4. Required FastAPI Routes

The backend should expose these routes:

```text
POST /labs/analyze
POST /imaging/analyze
POST /hospitals/referral
```

These are additional routes and must not change the existing frontend triage contract:

```text
POST /triage
```

The `/triage` response field names must remain unchanged.

---

# 5. Member 5 Module Files

Current Member 5 implementation:

```text
member5_work/
├── labs.py
├── imaging.py
├── hospitals.py
└── hospitals.json
```

For final backend integration, the backend developer can import or move these files into the backend structure.

Example:

```text
backend/
├── main.py
├── labs.py
├── imaging.py
├── hospitals.py
└── hospitals.json
```

---

# 6. Safety Requirements

All Member 5 modules are clinical decision-support prototypes.

They must not:

- Diagnose diseases autonomously
- Replace qualified healthcare professionals
- Claim medical certainty
- Provide prescriptions

All relevant disclaimers must be preserved.

---

# 7. Integration with FirstDoor

The complete flow should eventually be:

```text
Patient Input
     |
     v
FirstDoor Triage
     |
     +------------------+
     |                  |
     v                  v
Laboratory Module   Imaging Module
     |                  |
     +--------+---------+
              |
              v
       Risk Contribution
              |
              v
      Decision / Referral
              |
              v
       Hospital Directory
              |
              v
      Appropriate Specialty
```

---

# 8. Member 5 Completion Status

- [x] Laboratory analysis module
- [x] Laboratory abnormality detection
- [x] Imaging structured analysis module
- [x] Imaging risk contribution
- [x] Hospital referral system
- [x] Hospital dataset
- [x] API integration contract
- [x] GitHub backup

---

# 9. Triage Contract Update — Minor Support

The `/triage` backend must accept the following `risk_band` values:

```text
crisis
emergency
urgent
soon
routine
minor_support
```

## Minor Support Rule

For users under 18 on the emotional or mental-health pathway:

- The flow must stop before psychological screening.
- No psychological score should be generated.
- No referral should be generated.
- The response must use:

```json
{
  "risk_band": "minor_support"
}
```

Support contacts should be provided according to the frontend/backend contract.

This rule must be handled before normal psychological screening or scoring.