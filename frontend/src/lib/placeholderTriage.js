/**
 * PLACEHOLDER TRIAGE RULES — STRUCTURAL, NOT CLINICAL CONTENT.
 *
 * Everything in this file exists to give the intake page and the result page a
 * real, correctly-shaped object to pass between them. The option lists, the
 * point values, the band thresholds, the referral entries and the roadmap copy
 * are scaffolding. None of it has been authored or reviewed by a clinician and
 * none of it should be read as medical guidance.
 *
 * All of it is to be replaced by the team's authored rules table.
 *
 * Two properties must survive that replacement:
 *   1. FirstDoor does not diagnose and never names a medication.
 *   2. The red-flag check runs first and nothing downstream can override it.
 */

export const DURATION_OPTIONS = [
  { id: "under-24h", label: "Less than 24 hours", score: 1 },
  { id: "1-3-days", label: "One to three days", score: 2 },
  { id: "4d-2w", label: "Four days to two weeks", score: 3 },
  { id: "over-2w", label: "More than two weeks", score: 4 },
];

export const SEVERITY_OPTIONS = [
  { id: "mild", label: "Mild — I can carry on as usual", score: 1 },
  { id: "moderate", label: "Moderate — it is interfering with my day", score: 3 },
  { id: "severe", label: "Severe — I cannot do my usual activities", score: 5 },
];

export const AGE_OPTIONS = [
  { id: "under-18", label: "Under 18", score: 2 },
  { id: "18-39", label: "18 to 39", score: 0 },
  { id: "40-64", label: "40 to 64", score: 1 },
  { id: "65-plus", label: "65 or older", score: 3 },
];

export const RED_FLAGS = [
  { id: "chest", label: "Chest pain or pressure lasting more than a few minutes" },
  { id: "breathing", label: "Difficulty breathing, or breathlessness at rest" },
  { id: "stroke", label: "Sudden weakness, numbness, or trouble speaking" },
  { id: "bleeding", label: "Bleeding that will not stop, or vomiting blood" },
  { id: "conscious", label: "Fainting, confusion, or unresponsiveness" },
];

export const NONE_OF_THESE = {
  id: "none",
  label: "None of these apply",
};

const QUESTION_LABELS = {
  symptom: "What you described",
  duration: "How long it has been going on",
  severity: "How much it is affecting you",
  ageBand: "Age band",
  redFlag: "Emergency warning sign",
};

// Driver rows sit in a two-column layout on the result card, so a long free-text
// answer is trimmed for display. The full text stays in the intake state.
const DRIVER_TEXT_LIMIT = 100;

function forDisplay(text) {
  const clean = String(text ?? "").trim().replace(/\s+/g, " ");
  return clean.length > DRIVER_TEXT_LIMIT
    ? `${clean.slice(0, DRIVER_TEXT_LIMIT - 1)}…`
    : clean;
}

function lookup(options, id) {
  return options.find((o) => o.id === id) ?? null;
}

const BAND_CONTENT = {
  urgent: {
    headline: "Get seen within 48 hours.",
    referrals: [
      {
        specialty: "General medicine",
        rank: 1,
        rationale: "First point of contact for an in-person assessment within two days.",
      },
      {
        specialty: "Urgent care clinic",
        rank: 2,
        rationale: "If no general medicine appointment is available inside 48 hours.",
      },
    ],
    roadmap: [
      {
        stage: "Today",
        actions: [
          "Write down when the symptoms started and what makes them better or worse",
          "Go to an emergency department if any of the warning signs appear",
        ],
      },
      {
        stage: "Within 48 hours",
        actions: [
          "Book the appointment rather than waiting to see if it settles",
          "Bring a list of anything you are already taking",
        ],
      },
      {
        stage: "At the consultation",
        actions: [
          "Describe the timeline first, then the symptoms",
          "Ask what would need to change for you to come back sooner",
        ],
      },
    ],
  },
  soon: {
    headline: "Book an appointment this week.",
    referrals: [
      {
        specialty: "General medicine",
        rank: 1,
        rationale: "Best placed to examine you and decide whether a specialist is needed.",
      },
      {
        specialty: "Specialist referral",
        rank: 2,
        rationale: "Routed by general medicine once you have been examined.",
      },
    ],
    roadmap: [
      {
        stage: "Now",
        actions: [
          "Keep a short daily note of the symptoms and how they change",
          "Go to an emergency department if any of the warning signs appear",
        ],
      },
      {
        stage: "This week",
        actions: [
          "Book a general medicine appointment",
          "Bring the symptom notes with you",
        ],
      },
      {
        stage: "At the consultation",
        actions: [
          "Ask whether a specialist referral is needed",
          "Ask what should prompt you to return earlier",
        ],
      },
    ],
  },
  routine: {
    headline: "This can be handled as a routine visit.",
    referrals: [
      {
        specialty: "General medicine",
        rank: 1,
        rationale: "A routine appointment is enough unless the symptoms change.",
      },
    ],
    roadmap: [
      {
        stage: "Now",
        actions: [
          "Rest and keep an eye on whether anything changes",
          "Go to an emergency department if any of the warning signs appear",
        ],
      },
      {
        stage: "Over the next week",
        actions: [
          "Book a routine appointment if the symptoms have not settled",
          "Note anything new so you can describe it accurately",
        ],
      },
    ],
  },
};

const EMERGENCY_HEADLINE = "Go to an emergency department now.";

// Placeholder thresholds over a 2–12 point range.
const URGENT_AT = 9;
const SOON_AT = 6;

/**
 * Compute a triage result from the intake answers. Pure: same input, same
 * output, no I/O and no dependency on anything outside this module.
 *
 * @param {object} answers
 * @param {string} answers.symptom   Free-text description.
 * @param {string} answers.duration  DURATION_OPTIONS id.
 * @param {string} answers.severity  SEVERITY_OPTIONS id.
 * @param {string} answers.ageBand   AGE_OPTIONS id.
 * @param {string[]} answers.redFlags  RED_FLAGS ids that were ticked.
 * @returns {{
 *   risk_band: "emergency" | "urgent" | "soon" | "routine",
 *   headline: string,
 *   drivers: {question_id: string, answer: string}[],
 *   referrals: {specialty: string, rank: number, rationale: string}[],
 *   roadmap: {stage: string, actions: string[]}[],
 * }}
 */
export function computeTriage({ symptom, duration, severity, ageBand, redFlags = [] }) {
  const described = forDisplay(symptom);

  // ---------------------------------------------------------------------
  // RED-FLAG GATE. This runs before any scoring and returns immediately, so
  // no rule added below can downgrade an emergency. Keep it first.
  // ---------------------------------------------------------------------
  const ticked = RED_FLAGS.filter((flag) => redFlags.includes(flag.id));
  if (ticked.length > 0) {
    return {
      risk_band: "emergency",
      headline: EMERGENCY_HEADLINE,
      drivers: [
        ...ticked.map((flag) => ({
          question_id: QUESTION_LABELS.redFlag,
          answer: flag.label,
        })),
        { question_id: QUESTION_LABELS.symptom, answer: described },
      ],
      referrals: [],
      roadmap: [],
    };
  }

  // No red flags. Everything below is the placeholder scoring pass.
  const durationOption = lookup(DURATION_OPTIONS, duration);
  const severityOption = lookup(SEVERITY_OPTIONS, severity);
  const ageOption = lookup(AGE_OPTIONS, ageBand);

  const score =
    (durationOption?.score ?? 0) +
    (severityOption?.score ?? 0) +
    (ageOption?.score ?? 0);

  let risk_band = "routine";
  if (score >= URGENT_AT) risk_band = "urgent";
  else if (score >= SOON_AT) risk_band = "soon";

  const content = BAND_CONTENT[risk_band];

  return {
    risk_band,
    headline: content.headline,
    drivers: [
      { question_id: QUESTION_LABELS.symptom, answer: described },
      { question_id: QUESTION_LABELS.duration, answer: durationOption?.label ?? "Not answered" },
      { question_id: QUESTION_LABELS.severity, answer: severityOption?.label ?? "Not answered" },
      { question_id: QUESTION_LABELS.ageBand, answer: ageOption?.label ?? "Not answered" },
      { question_id: QUESTION_LABELS.redFlag, answer: NONE_OF_THESE.label },
    ],
    referrals: content.referrals,
    roadmap: content.roadmap,
  };
}
