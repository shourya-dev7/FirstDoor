/**
 * Backend transport for the physical triage path.
 */

import { AGE_OPTIONS } from "./placeholderTriage";

const BACKEND_URL = "https://firstdoor.onrender.com/api/assess";

const BACKEND_TIMEOUT_MS = 60000;

const API_SEVERITY = {
  mild: 3,
  moderate: 6,
  severe: 9,
};

function mapRiskLevel(riskLevel) {
  const level = String(riskLevel || "").toUpperCase();

  if (level === "EMERGENCY" || level === "CRITICAL") {
    return "emergency";
  }

  if (level === "HIGH") {
    return "urgent";
  }

  if (level === "MODERATE" || level === "MEDIUM") {
    return "soon";
  }

  return "routine";
}

function convertBackendResult(result, symptom) {
  if (!result || typeof result !== "object") {
    return null;
  }

  const risk_band = mapRiskLevel(result.risk_level);

  const drivers = [
    {
      question_id: "Risk score",
      answer:
        result.risk_score !== undefined
          ? `${result.risk_score}/100`
          : "Not available",
    },
    {
      question_id: "Urgency",
      answer: result.urgency || "Not available",
    },
  ];

  if (Array.isArray(result.red_flags) && result.red_flags.length > 0) {
    result.red_flags.forEach((flag) => {
      drivers.push({
        question_id: "Red flag",
        answer: String(flag),
      });
    });
  }

  const referrals = result.specialty
    ? [
        {
          specialty: result.specialty,
          rank: 1,
          rationale: "Suggested based on the reported symptoms and assessment.",
        },
      ]
    : [];

  const roadmap = [];

  if (
    Array.isArray(result.possible_conditions) &&
    result.possible_conditions.length > 0
  ) {
    roadmap.push({
      stage: "Possible conditions to discuss",
      actions: result.possible_conditions.map(String),
    });
  }

  if (
    Array.isArray(result.recommended_tests) &&
    result.recommended_tests.length > 0
  ) {
    roadmap.push({
      stage: "Possible tests to discuss",
      actions: result.recommended_tests.map(String),
    });
  }

  if (result.ai_explanation) {
    roadmap.push({
      stage: "Assessment explanation",
      actions: [String(result.ai_explanation)],
    });
  }

  return {
    risk_band,

    headline:
      result.urgency ||
      "Your assessment has been completed.",

    drivers,

    referrals,

    roadmap,

    crisis_support: null,

    // Preserve the complete backend response for future UI improvements.
    backend_data: result,

    symptom,
  };
}

export function isRenderableResult(value) {
  return Boolean(
    value &&
      typeof value === "object" &&
      typeof value.risk_band === "string" &&
      Array.isArray(value.drivers) &&
      Array.isArray(value.referrals) &&
      Array.isArray(value.roadmap)
  );
}

export async function fetchBackendTriage({
  symptom,
  duration,
  severity,
  ageBand,
  redFlags,
}) {
  const severityNumber = API_SEVERITY[severity];

  if (!severityNumber) return null;

  const ageLabel =
    AGE_OPTIONS.find((o) => o.id === ageBand)?.label ?? "";

  const ageMatch = ageLabel.match(/\d+/);

  const age = ageMatch
    ? Number(ageMatch[0])
    : 30;

  const controller = new AbortController();

  const timer = setTimeout(
    () => controller.abort(),
    BACKEND_TIMEOUT_MS
  );

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      signal: controller.signal,

      body: JSON.stringify({
        age,

        symptoms: [
          symptom.trim(),
        ],

        severity: severityNumber,

        duration,

        medical_history: [],

        red_flags: redFlags,
      }),
    });

    if (!response.ok) return null;

    const result = await response.json();

    const converted = convertBackendResult(
      result,
      symptom
    );

    return isRenderableResult(converted)
      ? converted
      : null;

  } catch (error) {
    console.warn(
      "FirstDoor: backend triage unavailable.",
      error
    );

    return null;

  } finally {
    clearTimeout(timer);
  }
}