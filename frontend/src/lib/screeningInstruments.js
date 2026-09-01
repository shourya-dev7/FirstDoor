/**
 * PHQ-9 AND GAD-7 — STRUCTURE ONLY. NO INSTRUMENT CONTENT IS AUTHORED HERE.
 *
 * The item wording, the 0-3 response scale labels, the severity cutoffs and
 * the severity band names below are all PLACEHOLDERS. Every one of them is
 * official content belonging to the source instrument. Writing plausible
 * substitutes would produce a fake questionnaire presented to people as a
 * validated one, so none of them have been written here.
 *
 * BEFORE THIS SHIPS, someone must:
 *   1. Paste the official item wording into every *_ITEM_*_TEXT string.
 *   2. Paste the official 0-3 frequency wording into every SCALE_LABEL_*.
 *   3. Fill PHQ9_SEVERITY_CUTOFFS and GAD7_SEVERITY_CUTOFFS from the
 *      instrument's own scoring guidance. Do not guess the numbers.
 *
 * The routing question below is ours, not instrument content, and is written.
 *
 * The placeholder strings render verbatim on screen on purpose. A screening
 * page that is obviously unconfigured is safe; one that looks finished but
 * carries invented wording is not.
 *
 * Two properties must survive that replacement:
 *   1. FirstDoor does not name a disorder and never names a medication.
 *   2. The crisis gate runs first and nothing downstream can override it.
 */

// TODO: official 0-3 frequency wording from the source instrument.
export const RESPONSE_SCALE = [
  { value: 0, label: "SCALE_LABEL_0" },
  { value: 1, label: "SCALE_LABEL_1" },
  { value: 2, label: "SCALE_LABEL_2" },
  { value: 3, label: "SCALE_LABEL_3" },
];

// TODO: official PHQ-9 item wording.
//
// Item 9 asks about thoughts of self-harm. It is marked with isCrisisItem so
// the gate in scoreScreening() finds it BY FLAG rather than by position — if
// these items are ever reordered, the gate follows the flag and stays attached
// to the right question. Moving the flag to the wrong item, or dropping it,
// changes safety behaviour. Do not edit it while pasting in the wording.
export const PHQ9_ITEMS = [
  { id: "phq9-1", text: "PHQ9_ITEM_1_TEXT" },
  { id: "phq9-2", text: "PHQ9_ITEM_2_TEXT" },
  { id: "phq9-3", text: "PHQ9_ITEM_3_TEXT" },
  { id: "phq9-4", text: "PHQ9_ITEM_4_TEXT" },
  { id: "phq9-5", text: "PHQ9_ITEM_5_TEXT" },
  { id: "phq9-6", text: "PHQ9_ITEM_6_TEXT" },
  { id: "phq9-7", text: "PHQ9_ITEM_7_TEXT" },
  { id: "phq9-8", text: "PHQ9_ITEM_8_TEXT" },
  { id: "phq9-9", text: "PHQ9_ITEM_9_TEXT", isCrisisItem: true },
];

// TODO: official GAD-7 item wording.
export const GAD7_ITEMS = [
  { id: "gad7-1", text: "GAD7_ITEM_1_TEXT" },
  { id: "gad7-2", text: "GAD7_ITEM_2_TEXT" },
  { id: "gad7-3", text: "GAD7_ITEM_3_TEXT" },
  { id: "gad7-4", text: "GAD7_ITEM_4_TEXT" },
  { id: "gad7-5", text: "GAD7_ITEM_5_TEXT" },
  { id: "gad7-6", text: "GAD7_ITEM_6_TEXT" },
  { id: "gad7-7", text: "GAD7_ITEM_7_TEXT" },
];

/**
 * TODO: fill from the source instrument's scoring guidance.
 *
 * Expected shape once authored — an array ordered low to high:
 *   [{ min: <number>, max: <number>, label: "<official band name>",
 *      risk_band: "routine" | "soon" | "urgent" }, ...]
 *
 * Left null until the real numbers and the real band names are pasted in.
 * While null, scoreScreening() reports the result as unscored rather than
 * inventing a band. Do not guess these.
 */
export const PHQ9_SEVERITY_CUTOFFS = null;
export const GAD7_SEVERITY_CUTOFFS = null;

export const INSTRUMENTS = {
  phq9: {
    id: "phq9",
    name: "PHQ-9",
    items: PHQ9_ITEMS,
    cutoffs: PHQ9_SEVERITY_CUTOFFS,
    // PHQ-9 carries a self-harm item, so a missing flag is a misconfiguration
    // and must fail closed rather than score. GAD-7 has no such item.
    expectsCrisisItem: true,
  },
  gad7: {
    id: "gad7",
    name: "GAD-7",
    items: GAD7_ITEMS,
    cutoffs: GAD7_SEVERITY_CUTOFFS,
    expectsCrisisItem: false,
  },
};

// Our own wording, not instrument content — these three strings are real
// user-facing text. The question routes between the two instruments in plain
// language, because nobody arriving here knows what PHQ-9 or GAD-7 are.
export const INSTRUMENT_ROUTING_QUESTION = "Which describes it better?";

export const INSTRUMENT_ROUTING_OPTIONS = [
  { id: "phq9", label: "Low mood, loss of interest, feeling down" },
  { id: "gad7", label: "Worry, tension, feeling on edge" },
];

// Verified contact details, not placeholders.
export const CRISIS_SUPPORT = [
  {
    name: "Tele-MANAS",
    numbers: ["14416", "1800-891-4416"],
    detail: "24/7 · free · available in 20 languages",
  },
];

const CRISIS_HEADLINE = "Support is available right now.";

// Driver rows sit in a two-column layout on the result card, so a long
// free-text answer is trimmed for display. Mirrors the helper in
// placeholderTriage.js; kept local so the two modules stay independent.
const DRIVER_TEXT_LIMIT = 100;

function forDisplay(text) {
  const clean = String(text ?? "").trim().replace(/\s+/g, " ");
  return clean.length > DRIVER_TEXT_LIMIT
    ? `${clean.slice(0, DRIVER_TEXT_LIMIT - 1)}…`
    : clean;
}

function crisisResult() {
  return {
    risk_band: "crisis",
    headline: CRISIS_HEADLINE,
    // Deliberately empty. Echoing back which item was answered how would put
    // someone's self-harm response on screen, and no score exists on this path.
    drivers: [],
    referrals: [],
    roadmap: [],
    crisis_support: CRISIS_SUPPORT,
  };
}

function bandForTotal(total, cutoffs) {
  if (!Array.isArray(cutoffs)) return null;
  return cutoffs.find((c) => total >= c.min && total <= c.max) ?? null;
}

// Referral is by care setting, not by condition. No disorder is named and no
// medication is mentioned on any path.
const SCREENING_REFERRALS = [
  {
    specialty: "Clinical psychology",
    rank: 1,
    rationale: "Assessment and talking-therapy options for how you have been feeling.",
  },
  {
    specialty: "Psychiatry",
    rank: 2,
    rationale: "If a medical assessment is needed alongside psychological support.",
  },
];

const SCREENING_ROADMAP = [
  {
    stage: "Now",
    actions: [
      "Tell someone you trust how you have been feeling",
      "Call Tele-MANAS on 14416 at any hour if things get worse",
    ],
  },
  {
    stage: "This week",
    actions: [
      "Book an appointment with a clinical psychologist or psychiatrist",
      "Bring this summary with you",
    ],
  },
  {
    stage: "At the consultation",
    actions: [
      "Say how long you have been feeling this way",
      "Ask what support options are open to you",
    ],
  },
];

/**
 * Score a completed screening questionnaire. Pure: same input, same output,
 * no I/O and no dependency on anything outside this module.
 *
 * @param {object} input
 * @param {string} input.instrument  Key into INSTRUMENTS ("phq9" | "gad7").
 * @param {Record<string, number>} input.responses  Item id -> 0..3.
 * @param {string} [input.symptom]  Free-text description.
 * @param {string} [input.ageBandLabel]  Already-resolved age band label.
 * @returns {{
 *   risk_band: "crisis" | "unscored" | "routine" | "soon" | "urgent",
 *   headline: string,
 *   drivers: {question_id: string, answer: string}[],
 *   referrals: {specialty: string, rank: number, rationale: string}[],
 *   roadmap: {stage: string, actions: string[]}[],
 *   crisis_support?: {name: string, numbers: string[], detail: string}[],
 * }}
 */
export function scoreScreening({ instrument, responses = {}, symptom, ageBandLabel }) {
  const spec = INSTRUMENTS[instrument] ?? null;

  // ---------------------------------------------------------------------
  // CRISIS GATE. This runs before any scoring and returns immediately, so no
  // rule added below can reach a person past it. Structurally identical to
  // the red-flag gate in placeholderTriage.js. Keep it first.
  //
  // It fails closed: an unknown instrument, a PHQ-9 whose self-harm item has
  // lost its isCrisisItem flag, or an unanswered crisis item all return the
  // crisis result rather than falling through to scoring.
  // ---------------------------------------------------------------------
  if (!spec) return crisisResult();

  const crisisItem = spec.items.find((item) => item.isCrisisItem) ?? null;
  if (spec.expectsCrisisItem && !crisisItem) return crisisResult();
  if (crisisItem && responses[crisisItem.id] !== 0) return crisisResult();

  // No crisis response. Everything below is ordinary scoring, and it is only
  // reachable because the gate above let it be.
  const total = spec.items.reduce((sum, item) => sum + (responses[item.id] ?? 0), 0);
  const maxTotal = spec.items.length * (RESPONSE_SCALE.length - 1);
  const band = bandForTotal(total, spec.cutoffs);

  const described = forDisplay(symptom);

  return {
    risk_band: band ? band.risk_band : "unscored",
    headline: band
      ? `Screening result: ${band.label}.`
      : "Your screening answers have been recorded.",
    drivers: [
      { question_id: "Screening used", answer: spec.name },
      // The total is only shown once a band exists to anchor it. An
      // unanchored number invites people to interpret it themselves.
      ...(band ? [{ question_id: `${spec.name} total`, answer: `${total} of ${maxTotal}` }] : []),
      ...(described ? [{ question_id: "What you described", answer: described }] : []),
      ...(ageBandLabel ? [{ question_id: "Age band", answer: ageBandLabel }] : []),
    ],
    referrals: SCREENING_REFERRALS,
    roadmap: SCREENING_ROADMAP,
  };
}
