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

# 9. Triage Contract Update — Minor Support

The `/triage` backend must support the following `risk_band` values:

```text
crisis | minor_support | emergency | urgent | soon | routine
```

## Emotional Path Gate Ordering

The emotional/mental-health pathway must apply these gates before any psychological screening or scoring.

### Gate 1 — Crisis Check

The crisis check runs first.

If a self-harm or crisis response is present, return:

```text
risk_band = crisis
```

This must happen even if the user is under 18.

Immediate crisis risk takes priority over the minor safeguarding pathway.

The crisis check must occur before scoring.

### Gate 2 — Minor Check

The minor check runs second.

If the user is:

- Under 18, or
- Has a missing age, or
- Has an unrecognised age band

the backend must fail closed and return:

```text
risk_band = minor_support
```

The flow must stop before any psychological instrument is administered.

No psychological screening score should be generated.

No referral should be generated.

## Exact Minor Support Response

```json
{
  "risk_band": "minor_support",
  "headline": "Please talk to an adult you trust.",
  "drivers": [],
  "referrals": [],
  "roadmap": [],
  "crisis_support": [
    {
        "name": "Tele-MANAS",
        "numbers": ["14416", "1800-891-4416"],
        "detail": "24/7, free, available in 20 languages"
    }
   ]
}
```

## Minor Support Rules

The following fields must always be present and must be empty arrays:

```json
"drivers": []
"referrals": []
"roadmap": []
```

They must never be:

- `null`
- missing
- objects
- strings

The frontend maps over these fields.

The existing `crisis_support` field is reused for `minor_support`.

No new support field should be created.

The response must not contain:

- a score
- a band number
- a severity value
- screening results

No screening answers exist because the minor gate runs before any psychological instrument is administered.

## Safety Ordering Summary

```text
Emotional Path
      |
      v
Crisis Check
      |
      |-- Crisis detected --> crisis response
      |
      v
Minor Check
      |
      |-- Under 18 / missing age / invalid age --> minor_support
      |
      v
Psychological Instrument
      |
      v
Scoring
      |
      v
Referral / Roadmap
```

The system fails closed for unknown or missing age information.