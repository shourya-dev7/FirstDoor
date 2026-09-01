/**
 * PHQ-9 AND GAD-7 — OFFICIAL INSTRUMENT CONTENT.
 *
 * The item wording, the 0-3 response scale labels, the shared prompt, the
 * severity cutoffs and the severity band names below are the official content
 * of the source instruments, reproduced verbatim. Both are public domain.
 *
 * Do not paraphrase, shorten, re-order or "improve" any of these strings. The
 * scores they produce are only meaningful for the exact wording that was
 * validated. Editing an item silently invalidates the instrument while leaving
 * the page looking finished, which is the failure this file is written to
 * prevent. Attribution is rendered on screen — see INSTRUMENT_ATTRIBUTION.
 *
 * The routing question and the risk_band mapping are ours, not instrument
 * content, and are marked as such where they appear.
 *
 * Two properties must survive any future edit:
 *   1. FirstDoor does not name a disorder and never names a medication.
 *   2. The crisis gate runs first and nothing downstream can override it.
 */

// Official 0-3 frequency wording. Shared by both instruments.
export const RESPONSE_SCALE = [
  { value: 0, label: "Not at all" },
  { value: 1, label: "Several days" },
  { value: 2, label: "More than half the days" },
  { value: 3, label: "Nearly every day" },
];

// Official prompt that both instruments are administered under. The two-week
// window is part of the instrument: the scores mean nothing without it, so it
// is rendered above the items rather than left implicit.
export const SHARED_PROMPT =
  "Over the last 2 weeks, how often have you been bothered by any of the " +
  "following problems?";

// Official PHQ-9 item wording.
//
// Item 9 asks about thoughts of self-harm. It is marked with isCrisisItem so
// the gate in scoreScreening() finds it BY FLAG rather than by position — if
// these items are ever reordered, the gate follows the flag and stays attached
// to the right question. Moving the flag to the wrong item, or dropping it,
// changes safety behaviour. Do not edit it.
export const PHQ9_ITEMS = [
  { id: "phq9-1", text: "Little interest or pleasure in doing things" },
  { id: "phq9-2", text: "Feeling down, depressed, or hopeless" },
  { id: "phq9-3", text: "Trouble falling or staying asleep, or sleeping too much" },
  { id: "phq9-4", text: "Feeling tired or having little energy" },
  { id: "phq9-5", text: "Poor appetite or overeating" },
  {
    id: "phq9-6",
    text:
      "Feeling bad about yourself — or that you are a failure or have let " +
      "yourself or your family down",
  },
  {
    id: "phq9-7",
    text:
      "Trouble concentrating on things, such as reading the newspaper or " +
      "watching television",
  },
  {
    id: "phq9-8",
    text:
      "Moving or speaking so slowly that other people could have noticed. Or " +
      "the opposite — being so fidgety or restless that you have been moving " +
      "around a lot more than usual",
  },
  {
    id: "phq9-9",
    text:
      "Thoughts that you would be better off dead, or of hurting yourself in " +
      "some way",
    isCrisisItem: true,
  },
];

// Official GAD-7 item wording.
export const GAD7_ITEMS = [
  { id: "gad7-1", text: "Feeling nervous, anxious, or on edge" },
  { id: "gad7-2", text: "Not being able to stop or control worrying" },
  { id: "gad7-3", text: "Worrying too much about different things" },
  { id: "gad7-4", text: "Trouble relaxing" },
  { id: "gad7-5", text: "Being so restless that it's hard to sit still" },
  { id: "gad7-6", text: "Becoming easily annoyed or irritable" },
  { id: "gad7-7", text: "Feeling afraid as if something awful might happen" },
];

/**
 * Severity bands from each instrument's own scoring guidance.
 *
 * `min`, `max` and `label` are official instrument content — the ranges and
 * the band names are fixed by the source and are not ours to adjust.
 *
 * `risk_band` is NOT instrument content. Neither questionnaire says how
 * urgently someone should be seen; that is FirstDoor's routing decision,
 * mapping a severity onto the three urgency bands the result screen renders.
 * It follows the usual convention that a score of 10 or more is the threshold
 * for clinical attention, so:
 *   minimal / mild        -> routine
 *   moderate              -> soon
 *   moderately severe     -> urgent
 *   severe                -> urgent
 * NEEDS CLINICAL SIGN-OFF before this is put in front of the public. Changing
 * a risk_band here changes how urgently a real person is told to seek care.
 * The band names and ranges beside it must not be changed at all.
 */
export const PHQ9_SEVERITY_CUTOFFS = [
  { min: 0, max: 4, label: "Minimal", risk_band: "routine" },
  { min: 5, max: 9, label: "Mild", risk_band: "routine" },
  { min: 10, max: 14, label: "Moderate", risk_band: "soon" },
  { min: 15, max: 19, label: "Moderately severe", risk_band: "urgent" },
  { min: 20, max: 27, label: "Severe", risk_band: "urgent" },
];

export const GAD7_SEVERITY_CUTOFFS = [
  { min: 0, max: 4, label: "Minimal", risk_band: "routine" },
  { min: 5, max: 9, label: "Mild", risk_band: "routine" },
  { min: 10, max: 14, label: "Moderate", risk_band: "soon" },
  { min: 15, max: 21, label: "Severe", risk_band: "urgent" },
];

// Rendered under the questionnaire. Both instruments are public domain, but
// the attribution is still shown: it tells a reader what they were given and
// who validated it. Do not drop it.
export const INSTRUMENT_ATTRIBUTION =
  "PHQ-9 and GAD-7 developed by Drs. Robert L. Spitzer, Janet B.W. Williams, " +
  "Kurt Kroenke and colleagues, with an educational grant from Pfizer Inc. " +
  "Public domain — no permission required to reproduce.";

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

// A minor is not screened for a mental health condition without an adult in
// the loop, so the emotional path halts before either instrument is
// administered. The id — not the display label — is matched: the label is
// user-facing copy, and rewording it must not be able to silently switch a
// safety gate off.
export const MINOR_AGE_BAND_ID = "under-18";

// The gate below fails closed against THIS list rather than testing for the
// minor id, so a missing, misspelled or unrecognised age band halts too. Any
// age band added to AGE_OPTIONS and not added here therefore fails safe: it
// halts rather than scores, which is the direction a drift should break in.
const ADULT_AGE_BAND_IDS = ["18-39", "40-64", "65-plus"];

const MINOR_SUPPORT_HEADLINE = "Please talk to an adult you trust.";

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

// Mirrors crisisResult(): no score, no band, no referral and no drivers. The
// screening was never administered, so there is nothing to echo back.
function minorSupportResult() {
  return {
    risk_band: "minor_support",
    headline: MINOR_SUPPORT_HEADLINE,
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
 * @param {string} [input.ageBand]  AGE_OPTIONS id. Drives the minor gate; the
 *   stable id is used rather than the label so rewording copy cannot disable it.
 * @param {string} [input.ageBandLabel]  Already-resolved age band label. Display
 *   only — never gated on.
 * @returns {{
 *   risk_band: "crisis" | "minor_support" | "unscored" | "routine" | "soon"
 *     | "urgent",
 *   headline: string,
 *   drivers: {question_id: string, answer: string}[],
 *   referrals: {specialty: string, rank: number, rationale: string}[],
 *   roadmap: {stage: string, actions: string[]}[],
 *   crisis_support?: {name: string, numbers: string[], detail: string}[],
 * }}
 */
export function scoreScreening({
  instrument,
  responses = {},
  symptom,
  ageBand,
  ageBandLabel,
}) {
  const spec = INSTRUMENTS[instrument] ?? null;

  // ---------------------------------------------------------------------
  // CRISIS GATE. This runs before any scoring and returns immediately, so no
  // rule added below can reach a person past it. Structurally identical to
  // the red-flag gate in placeholderTriage.js. Keep it first.
  //
  // It fails closed: an unknown instrument, a PHQ-9 whose self-harm item has
  // lost its isCrisisItem flag, or an unanswered crisis item all return the
  // crisis result rather than falling through to scoring. The unanswered case
  // is checked below the minor gate — see the split note further down.
  // ---------------------------------------------------------------------
  if (!spec) return crisisResult();

  const crisisItem = spec.items.find((item) => item.isCrisisItem) ?? null;
  if (spec.expectsCrisisItem && !crisisItem) return crisisResult();

  // The gate is split in two around the minor gate below, because "answered
  // with a non-zero value" and "not answered at all" must not be treated the
  // same once minors stop being administered the items.
  //
  // An ACTUAL crisis response outranks everything, including the minor gate:
  // a person at acute risk gets the crisis screen whatever their age.
  const crisisAnswer = crisisItem ? responses[crisisItem.id] : undefined;
  const crisisAnswered = crisisAnswer !== undefined && crisisAnswer !== null
    && crisisAnswer !== "";
  if (crisisItem && crisisAnswered && Number(crisisAnswer) !== 0) return crisisResult();

  // ---------------------------------------------------------------------
  // MINOR GATE. Runs second, so an acute-risk answer is never suppressed by
  // it — a person in crisis gets the crisis screen whatever their age. Like
  // the gate above it returns before any scoring exists, and it fails closed:
  // only an explicitly recognised adult band is allowed through, so a missing
  // or unknown age band halts rather than scores.
  //
  // The intake also stops before showing any items to a minor. This gate is
  // the backstop for that, not a substitute: it is what makes a direct call
  // to scoreScreening() safe.
  // ---------------------------------------------------------------------
  if (!ADULT_AGE_BAND_IDS.includes(ageBand)) return minorSupportResult();

  // Second half of the crisis gate. A minor never reaches this line, which is
  // the point: the intake shows them no items, so their crisis item is always
  // unanswered, and without the split below they would be routed to the
  // crisis screen purely for not having been asked. For an adult an
  // unanswered or unparseable crisis item still fails closed to crisis.
  if (crisisItem && (!crisisAnswered || Number.isNaN(Number(crisisAnswer)))) {
    return crisisResult();
  }

  // No crisis response and an adult respondent. Everything below is ordinary
  // scoring, and it is only reachable because both gates above let it be.
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
