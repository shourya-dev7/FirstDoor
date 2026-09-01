/**
 * Optional backend transport for the physical triage path.
 *
 * The backend runs on a developer's machine, not at the deployed URL, so the
 * published site must produce a result without it. Nothing here is allowed to
 * become required: every failure returns null and the caller falls back to the
 * local triage in placeholderTriage.js.
 *
 * Kept out of the page component so the guard and the transport can be
 * exercised directly.
 */
import { AGE_OPTIONS } from "./placeholderTriage";

const BACKEND_URL = "https://firstdoor.onrender.com/api/assess";

// A connection to a port nothing is listening on usually fails fast, but a
// firewall can leave it hanging instead. Without a deadline the submit button
// would stay disabled indefinitely on the deployed site.
const BACKEND_TIMEOUT_MS = 20000;

// Severity is collected as an option id ("mild"), and the backend's schema
// requires an integer from 1 to 10. These are spread across that range rather
// than reusing the local scoring weights, which only go up to 5.
const API_SEVERITY = { mild: 3, moderate: 6, severe: 9 };

// The result screen reads these fields directly: it indexes a colour map with
// risk_band and maps over the three arrays. A response missing any of them
// cannot be rendered whatever status code carried it, so it counts as a
// failure and the local triage is used instead.
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

// Returns a renderable result, or null if the backend could not supply one.
// Resolves to null for every expected failure rather than throwing: an absent
// backend is the normal state at the deployed URL, not an exception.
export async function fetchBackendTriage({ symptom, duration, severity, ageBand, redFlags }) {
  const severityNumber = API_SEVERITY[severity];
  if (!severityNumber) return null;

  // The backend takes a number; the intake collects a band. The lower bound of
  // the selected band is the honest reading of it — it does not invent a
  // precision the question never asked for.
  const ageLabel = AGE_OPTIONS.find((o) => o.id === ageBand)?.label ?? "";
  const ageMatch = ageLabel.match(/\d+/);
  const age = ageMatch ? Number(ageMatch[0]) : 30;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), BACKEND_TIMEOUT_MS);

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
      body: JSON.stringify({
        age,
        symptoms: [symptom.trim()],
        severity: severityNumber,
        duration,

        // No medical history is currently collected by this intake form.
        medical_history: [],
        red_flags: redFlags,
      }),
    });

    if (!response.ok) return null;

    const result = await response.json();
    return isRenderableResult(result) ? result : null;
  } catch (error) {
    // Connection refused, DNS failure, mixed-content block, the abort above,
    // or a body that is not JSON. Every one of them means "no usable result
    // from the backend", which is exactly what null says.
    console.warn("FirstDoor: backend triage unavailable.", error);
    return null;
  } finally {
    clearTimeout(timer);
  }
}
