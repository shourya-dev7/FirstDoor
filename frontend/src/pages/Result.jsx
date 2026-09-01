import { useState } from "react";
import { Link, useLocation } from "react-router-dom";

const SAMPLE = {
  risk_band: "urgent",
  headline: "See a pulmonologist within 48 hours.",
  drivers: [
    { question_id: "Cough duration", answer: "3 weeks", weight: 3 },
    { question_id: "Weight change", answer: "Unintentional loss", weight: 3 },
    { question_id: "Blood in sputum", answer: "Occasionally", weight: 4 },
  ],
  referrals: [
    { specialty: "Pulmonology", rank: 1, rationale: "Persistent cough with blood and weight loss" },
    { specialty: "General medicine", rank: 2, rationale: "If pulmonology access is delayed" },
  ],
  roadmap: [
    { stage: "Now", actions: ["Keep a written symptom diary", "Go to hospital today if breathing becomes difficult"] },
    { stage: "Within 48 hours", actions: ["Book the pulmonology consult", "Carry any prior chest imaging"] },
    { stage: "At the consultation", actions: ["Expect a chest X-ray", "Expect sputum testing"] },
  ],
};

const SAMPLE_EMERGENCY = {
  risk_band: "emergency",
  headline: "Go to an emergency department now.",
  drivers: [
    { question_id: "Chest pain", answer: "Radiating to left arm", weight: 5 },
    { question_id: "Onset", answer: "2 hours ago", weight: 4 },
  ],
  referrals: [],
  roadmap: [],
};

const BAND = {
  emergency: { label: "Emergency", fg: "#B4442C", bg: "#FBEAE4", line: "#E0AF9E" },
  urgent: { label: "Urgent", fg: "#8A5A12", bg: "#FBF2E2", line: "#DFC894" },
  soon: { label: "See a doctor soon", fg: "#1F6A7A", bg: "#E4F1F4", line: "#A9CDD6" },
  routine: { label: "Routine", fg: "#0B6B57", bg: "#E6F4EE", line: "#A6CFBF" },
  // A completed screening whose severity cutoffs have not been configured yet.
  // No band is invented for it.
  unscored: { label: "Not scored", fg: "#48605F", bg: "#EFEDE4", line: "#DAD4C4" },
  // Listed for completeness. The minor-support result renders through the
  // crisis layout below, which shows no band chip, so this is never read.
  minor_support: { label: "Support", fg: "#1F6A7A", bg: "#E4F1F4", line: "#A9CDD6" },
};

// Bands that represent a screening actually carried through to a severity.
// "unscored", "crisis" and "minor_support" are not in here: none is an
// outcome of the two-step flow, so none gets the step counter in the header.
const SCORED_BANDS = ["emergency", "urgent", "soon", "routine"];

export default function Result() {
  const location = useLocation();
  // A real result only ever arrives from Intake via router state. Opening
  // /result directly must NOT show a fabricated result for symptoms nobody
  // entered — it shows the empty state until a sample is explicitly loaded.
  const fromIntake = location.state?.result ?? null;
  const [preview, setPreview] = useState(null);

  const data = fromIntake ?? preview;
  // The crisis result carries no band, no score and no referral, so it is
  // checked before BAND is read and renders its own card below.
  const isCrisis = data?.risk_band === "crisis";
  // A minor is never screened, so this result has nothing to score either. It
  // reuses the crisis layout: a message, the helplines, and nothing else.
  const isMinor = data?.risk_band === "minor_support";
  const isHalted = isCrisis || isMinor;
  const band = data && !isHalted ? BAND[data.risk_band] : null;
  const isEmergency = data?.risk_band === "emergency";
  const isScored = SCORED_BANDS.includes(data?.risk_band);

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #06262E; }
        .rs { min-height: 100vh; background: #06262E; color: #EAF4F5;
              font-family: 'IBM Plex Sans', system-ui, sans-serif; }
        .rs-bar { display: flex; justify-content: space-between; align-items: center;
                  padding: 20px 6vw; border-bottom: 1px solid #12414C; }
        .rs-mark { display: inline-block; font-family: 'Instrument Serif', serif; font-size: 28px;
                   color: inherit; text-decoration: none; border-radius: 4px; }
        .rs-mark span { color: #02C39A; }
        .rs-mark:hover { color: #02C39A; }
        .rs-mark:focus-visible { outline: 2px solid #02C39A; outline-offset: 3px; }
        .rs-step { font-size: 11.5px; letter-spacing: .14em; text-transform: uppercase; color: #6E959E; }
        .rs-wrap { max-width: 780px; margin: 0 auto; padding: 6vh 5vw 10vh; }
        .rs-card { background: #F4F1E9; color: #123038; border-radius: 14px;
                   padding: 34px; box-shadow: 0 24px 60px rgba(0,0,0,.34); }
        .rs-band { display: inline-block; font-size: 11.5px; font-weight: 600;
                   letter-spacing: .13em; text-transform: uppercase; padding: 7px 13px; border-radius: 5px; }
        .rs-head { font-family: 'Instrument Serif', serif; font-size: 34px;
                   line-height: 1.15; margin-top: 18px; }
        .rs-lead { margin-top: 12px; font-size: 16px; line-height: 1.6; color: #48605F; }
        .rs-sec { margin-top: 34px; padding-top: 26px; border-top: 1px solid #DAD4C4; }
        .rs-label { font-size: 10.5px; letter-spacing: .16em; text-transform: uppercase;
                    color: #6D7E7F; font-weight: 600; margin-bottom: 16px; }
        .rs-driver { display: flex; justify-content: space-between; gap: 16px;
                     padding: 11px 0; border-bottom: 1px dashed #DFDACB; font-size: 15px; }
        .rs-driver:last-child { border-bottom: none; }
        .rs-dq { color: #6F7E7E; }
        .rs-da { font-weight: 500; text-align: right; }
        .rs-ref { display: flex; gap: 15px; padding: 14px 0; border-bottom: 1px solid #E6E1D3; }
        .rs-ref:last-child { border-bottom: none; }
        .rs-rank { font-family: 'Instrument Serif', serif; font-size: 25px; color: #B6AE99;
                   line-height: 1; width: 26px; flex-shrink: 0; }
        .rs-spec { font-size: 18px; font-weight: 600; }
        .rs-why { font-size: 14px; color: #6F7E7E; margin-top: 3px; line-height: 1.5; }
        .rs-stage { margin-bottom: 20px; }
        .rs-stage:last-child { margin-bottom: 0; }
        .rs-sname { font-size: 15px; font-weight: 600; margin-bottom: 6px; }
        .rs-act { font-size: 14.5px; color: #526A69; line-height: 1.65; padding-left: 15px;
                  position: relative; }
        .rs-act::before { content: "—"; position: absolute; left: 0; color: #B6AE99; }
        .rs-warn { margin-top: 26px; font-size: 14px; line-height: 1.6; color: #6F7E7E;
                   border-left: 2px solid #DAD4C4; padding-left: 13px; }
        .rs-foot { text-align: center; margin-top: 26px; font-size: 12.5px; color: #55808A; }
        .rs-toggle { background: none; border: 1px solid #1B4E59; color: #7FA9B2;
                     font: inherit; font-size: 12px; padding: 6px 13px; border-radius: 999px;
                     cursor: pointer; margin-top: 14px; }
        .rs-toggle:hover { border-color: #02C39A; color: #02C39A; }
        .rs-toggle:focus-visible { outline: 2px solid #02C39A; outline-offset: 2px; }
        .rs-empty-head { font-family: 'Instrument Serif', serif; font-size: 34px; line-height: 1.15; }
        .rs-empty-lead { margin-top: 12px; font-size: 16px; line-height: 1.6; color: #48605F; max-width: 46ch; }
        .rs-cta { display: inline-block; margin-top: 24px; font: inherit; font-size: 15.5px;
                  font-weight: 600; color: #06262E; background: #02C39A; border-radius: 9px;
                  padding: 14px 26px; text-decoration: none; }
        .rs-cta:hover { background: #04D8AB; }
        .rs-cta:focus-visible { outline: 2px solid #123038; outline-offset: 3px; }
        .rs-ghost { background: none; border: 1px solid #DAD4C4; color: #6F7E7E; font: inherit;
                    font-size: 12.5px; padding: 7px 14px; border-radius: 999px; cursor: pointer; }
        .rs-ghost:hover { border-color: #B6AE99; color: #48605F; }
        .rs-ghost:focus-visible { outline: 2px solid #123038; outline-offset: 2px; }
        .rs-dev { margin-top: 30px; padding-top: 22px; border-top: 1px solid #DAD4C4; }
        .rs-crisis-head { font-family: 'Instrument Serif', serif; font-size: 34px; line-height: 1.15; }
        .rs-crisis-lead { margin-top: 12px; font-size: 16.5px; line-height: 1.6; color: #48605F;
                          max-width: 48ch; }
        .rs-help { margin-top: 26px; background: #FBEAE4; border: 1px solid #E0AF9E;
                   border-left: 3px solid #B4442C; border-radius: 11px; padding: 22px 24px; }
        .rs-help-name { font-size: 18px; font-weight: 600; color: #123038; }
        .rs-help-detail { font-size: 13.5px; color: #8A5344; margin-top: 3px; }
        .rs-tels { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
        .rs-tel { font-family: 'Instrument Serif', serif; font-size: 30px; line-height: 1;
                  color: #B4442C; text-decoration: none; background: #FDF4F1;
                  border: 1px solid #E7C4B7; border-radius: 9px; padding: 12px 18px; }
        .rs-tel:hover { background: #F9E4DD; border-color: #B4442C; }
        .rs-tel:focus-visible { outline: 2px solid #B4442C; outline-offset: 3px; }
        .rs-crisis-note { margin-top: 22px; font-size: 14.5px; line-height: 1.6; color: #6F7E7E;
                          border-left: 2px solid #DAD4C4; padding-left: 13px; }
        @media (max-width: 600px) {
          .rs-crisis-head { font-size: 27px; }
          .rs-tel { font-size: 26px; }
          .rs-help { padding: 20px 17px; }
          .rs-card { padding: 24px; }
          .rs-head { font-size: 27px; }
          .rs-empty-head { font-size: 27px; }
          .rs-cta { width: 100%; text-align: center; }
          .rs-driver { flex-direction: column; gap: 2px; }
          .rs-da { text-align: left; }
        }
      `}</style>

      <div className="rs">
        <header className="rs-bar">
          <Link className="rs-mark" to="/">First<span>Door</span></Link>
          {isScored && <div className="rs-step">Step 2 of 2 · Result</div>}
        </header>

        <div className="rs-wrap">
          {!data && (
            <div className="rs-card">
              <h1 className="rs-empty-head">No result yet.</h1>
              <p className="rs-empty-lead">
                Your result appears here once you have completed the intake — five short
                questions about what you are feeling and how long it has been going on.
              </p>
              <Link className="rs-cta" to="/intake">Start the intake</Link>

              <div className="rs-dev">
                <button className="rs-ghost" onClick={() => setPreview(SAMPLE)}>
                  Preview a sample result
                </button>
              </div>
            </div>
          )}

          {data && isHalted && (
            <div className="rs-card">
              <h1 className="rs-crisis-head">{data.headline}</h1>
              <p className="rs-crisis-lead">
                {isMinor
                  ? "A parent, guardian, school counsellor or your GP can help you work out what to do next — you do not have to raise it alone. If you would rather speak to someone outside that, these lines are free and answered at any hour."
                  : "You do not have to work out what to do next on your own. These lines are answered by trained people, at any hour, and the call is free."}
              </p>

              {(data.crisis_support ?? []).map((service) => (
                <div className="rs-help" key={service.name}>
                  <p className="rs-help-name">{service.name}</p>
                  <p className="rs-help-detail">{service.detail}</p>
                  <div className="rs-tels">
                    {service.numbers.map((number) => (
                      <a className="rs-tel" href={`tel:${number.replace(/[^0-9+]/g, "")}`} key={number}>
                        {number}
                      </a>
                    ))}
                  </div>
                </div>
              ))}

              {!isMinor && (
                <p className="rs-crisis-note">
                  If you are in immediate danger, call your local emergency number, or ask
                  someone nearby to stay with you.
                </p>
              )}
            </div>
          )}

          {data && !isHalted && (
          <div className="rs-card">
            <span
              className="rs-band"
              style={{ color: band.fg, background: band.bg, boxShadow: `inset 0 0 0 1px ${band.line}` }}
            >
              {band.label}
            </span>

            <h1 className="rs-head">{data.headline}</h1>

            {isEmergency ? (
              <>
                <p className="rs-lead">
                  Your answers matched a red-flag rule. Do not wait for an appointment and do not
                  drive yourself. Call your local emergency number or ask someone to take you.
                </p>
              </>
            ) : (
              <>
                <p className="rs-lead">
                  This is not a diagnosis. It is an assessment of how urgent your symptoms are and
                  which specialist is best placed to look at them.
                </p>
              </>
            )}

            <section className="rs-sec">
              <p className="rs-label">Why this result</p>
              {data.drivers.map((d, n) => (
                <div className="rs-driver" key={n}>
                  <span className="rs-dq">{d.question_id}</span>
                  <span className="rs-da">{d.answer}</span>
                </div>
              ))}
            </section>

            {!isEmergency && data.referrals.length > 0 && (
              <section className="rs-sec">
                <p className="rs-label">Who to see</p>
                {data.referrals.map((r) => (
                  <div className="rs-ref" key={r.rank}>
                    <span className="rs-rank">{r.rank}</span>
                    <div>
                      <p className="rs-spec">{r.specialty}</p>
                      <p className="rs-why">{r.rationale}</p>
                    </div>
                  </div>
                ))}
              </section>
            )}

            {!isEmergency && data.roadmap.length > 0 && (
              <section className="rs-sec">
                <p className="rs-label">What happens next</p>
                {data.roadmap.map((s, n) => (
                  <div className="rs-stage" key={n}>
                    <p className="rs-sname">{s.stage}</p>
                    {s.actions.map((a, m) => (
                      <p className="rs-act" key={m}>{a}</p>
                    ))}
                  </div>
                ))}
              </section>
            )}

            <p className="rs-warn">
              FirstDoor does not diagnose conditions and does not recommend medication.
              Bring this summary to your consultation.
            </p>
          </div>
          )}

          {data && !isHalted && !fromIntake && (
            <p className="rs-foot">
              <button
                className="rs-toggle"
                onClick={() => setPreview(isEmergency ? SAMPLE : SAMPLE_EMERGENCY)}
              >
                Preview {isEmergency ? "urgent" : "emergency"} result
              </button>
            </p>
          )}
        </div>
      </div>
    </>
  );
}