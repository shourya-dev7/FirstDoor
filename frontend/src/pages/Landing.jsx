import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const CASES = [
  {
    symptom: "Chest tightness for two hours, spreading to the left arm",
    band: "Emergency",
    route: "Go to an emergency department now",
    note: "Matched a red-flag rule. No model was called.",
    tone: "alarm",
  },
  {
    symptom: "Cough for three weeks, occasional blood, losing weight",
    band: "Urgent",
    route: "Pulmonology — within 48 hours",
    note: "Duration and weight loss together raised the band.",
    tone: "warn",
  },
  {
    symptom: "Headache most mornings for two weeks, blurred vision",
    band: "Soon",
    route: "Neurology — book this week",
    note: "Morning pattern with visual change drove the routing.",
    tone: "warn",
  },
  {
    symptom: "Sore throat since yesterday, no fever, eating normally",
    band: "Routine",
    route: "Self-care — return if it passes five days",
    note: "No red flags. Resolved without escalation.",
    tone: "calm",
  },
];

const TONE = {
  alarm: { fg: "#B4442C", bg: "#FBEAE4", line: "#E0AF9E" },
  warn: { fg: "#8A5A12", bg: "#FBF2E2", line: "#DFC894" },
  calm: { fg: "#0B6B57", bg: "#E6F4EE", line: "#A6CFBF" },
};

export default function Landing() {
  const [i, setI] = useState(0);
  const [phase, setPhase] = useState("reading");

  useEffect(() => {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) {
      setPhase("done");
      return;
    }
    let t1, t2;
    setPhase("reading");
    t1 = setTimeout(() => setPhase("done"), 1400);
    t2 = setTimeout(() => setI((n) => (n + 1) % CASES.length), 7200);
    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
    };
  }, [i]);

  const c = CASES[i];
  const tone = TONE[c.tone];

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #06262E; }
        .fd {
          min-height: 100vh;
          background: #06262E;
          color: #EAF4F5;
          font-family: 'IBM Plex Sans', system-ui, sans-serif;
          display: flex;
          flex-direction: column;
        }
        .fd-bar {
          display: flex; justify-content: space-between; align-items: center;
          padding: 22px 6vw; border-bottom: 1px solid #12414C;
        }
        .fd-mark { font-family: 'Instrument Serif', serif; font-size: 60px; letter-spacing: .01em; }
        .fd-mark span { color: #02C39A; }
        .fd-team { font-size: 12px; color: #6E959E; letter-spacing: .08em; text-transform: uppercase; }
        .fd-main {
          flex: 1; display: grid; grid-template-columns: 1.05fr .95fr;
          gap: 5vw; align-items: center; padding: 7vh 6vw;
        }
        .fd-eyebrow {
          font-size: 11.5px; letter-spacing: .18em; text-transform: uppercase;
          color: #02C39A; font-weight: 600; margin-bottom: 22px;
        }
        .fd-h1 {
          font-family: 'Instrument Serif', serif; font-weight: 400;
          font-size: clamp(42px, 5.4vw, 78px); line-height: 1.02; letter-spacing: -.015em;
        }
        .fd-h1 em { font-style: italic; color: #02C39A; }
        .fd-sub {
          margin-top: 26px; font-size: 17px; line-height: 1.6;
          color: #9FC9CE; max-width: 44ch;
        }
        .fd-rule { width: 52px; height: 2px; background: #02C39A; margin: 34px 0 26px; }
        .fd-cta {
          display: inline-block; font-size: 15.5px; font-weight: 600; color: #06262E;
          background: #02C39A; border-radius: 9px; padding: 14px 26px;
          text-decoration: none; margin-bottom: 26px;
        }
        .fd-cta:hover { background: #04D8AB; }
        .fd-cta:focus-visible { outline: 2px solid #EAF4F5; outline-offset: 3px; }
        .fd-cta-note { display: inline-block; font-size: 13px; color: #6E959E; margin: 0 0 26px 16px; }
        .fd-facts { display: flex; flex-wrap: wrap; gap: 10px; }
        .fd-chip {
          font-size: 12.5px; color: #B9D9DD; border: 1px solid #1B4E59;
          border-radius: 999px; padding: 7px 14px;
        }
        .fd-panel {
          background: #F4F1E9; color: #123038; border-radius: 14px;
          padding: 30px 30px 26px; box-shadow: 0 24px 60px rgba(0,0,0,.34);
        }
        .fd-panel-top {
          display: flex; justify-content: space-between; align-items: baseline;
          border-bottom: 1px solid #DAD4C4; padding-bottom: 14px; margin-bottom: 20px;
        }
        .fd-panel-label {
          font-size: 10.5px; letter-spacing: .16em; text-transform: uppercase;
          color: #6D7E7F; font-weight: 600;
        }
        .fd-count { font-size: 11px; color: #97A3A2; font-variant-numeric: tabular-nums; }
        .fd-quote {
          font-family: 'Instrument Serif', serif; font-size: 25px; line-height: 1.3;
          min-height: 2.6em;
        }
        .fd-verdict { margin-top: 22px; min-height: 132px; }
        .fd-reading { display: flex; align-items: center; gap: 9px; padding-top: 12px; }
        .fd-dot {
          width: 6px; height: 6px; border-radius: 50%; background: #9AA6A5;
          animation: fdp 1s infinite ease-in-out;
        }
        .fd-dot:nth-child(2) { animation-delay: .16s; }
        .fd-dot:nth-child(3) { animation-delay: .32s; }
        .fd-reading span { font-size: 13px; color: #7C8A89; margin-left: 4px; }
        @keyframes fdp { 0%,100% { opacity:.25 } 50% { opacity:1 } }
        .fd-out { animation: fdin .5s ease both; }
        @keyframes fdin { from { opacity:0; transform: translateY(7px) } to { opacity:1; transform:none } }
        .fd-band {
          display: inline-block; font-size: 11.5px; font-weight: 600;
          letter-spacing: .13em; text-transform: uppercase;
          padding: 6px 12px; border-radius: 5px;
        }
        .fd-route { margin-top: 14px; font-size: 19px; font-weight: 500; }
        .fd-note {
          margin-top: 10px; font-size: 13.5px; color: #6F7E7E; line-height: 1.5;
          border-left: 2px solid #DAD4C4; padding-left: 11px;
        }
        .fd-foot {
          padding: 18px 6vw 30px; font-size: 12.5px; color: #55808A;
          border-top: 1px solid #12414C;
        }
        @media (max-width: 900px) {
          .fd-main { grid-template-columns: 1fr; gap: 42px; padding: 6vh 6vw; }
          .fd-quote { font-size: 21px; }
        }
        @media (prefers-reduced-motion: reduce) {
          .fd-dot, .fd-out { animation: none; }
        }
      `}</style>

      <div className="fd">
        <header className="fd-bar">
          <div className="fd-mark">First<span>Door</span></div>
          <div className="fd-team">Semi-colon Survivors</div>
        </header>

        <main className="fd-main">
          <section>
            <h1 className="fd-h1">
              Most people wait<br />because nobody tells<br />them <em>which door</em>.
            </h1>
            <p className="fd-sub">
              FirstDoor reads a symptom the way a triage nurse would: how urgent is this,
              and who should see it. It does not name a disease and it does not suggest a medicine.
            </p>
            <div className="fd-rule" />
            <Link className="fd-cta" to="/intake">Start a triage</Link>
            <span className="fd-cta-note">Five questions, about a minute.</span>
            <div className="fd-facts">
              <span className="fd-chip">Red-flag rules run before the model</span>
              <span className="fd-chip">Twelve referral specialties</span>
              <span className="fd-chip">Every score shows its reasoning</span>
            </div>
          </section>

          <section className="fd-panel">
            <div className="fd-panel-top">
              <span className="fd-panel-label">Triage, worked through</span>
              <span className="fd-count">{i + 1} / {CASES.length}</span>
            </div>

            <p className="fd-quote">&ldquo;{c.symptom}&rdquo;</p>

            <div className="fd-verdict">
              {phase === "reading" ? (
                <div className="fd-reading">
                  <i className="fd-dot" /><i className="fd-dot" /><i className="fd-dot" />
                  <span>Checking red-flag rules</span>
                </div>
              ) : (
                <div className="fd-out">
                  <span
                    className="fd-band"
                    style={{ color: tone.fg, background: tone.bg, boxShadow: `inset 0 0 0 1px ${tone.line}` }}
                  >
                    {c.band}
                  </span>
                  <p className="fd-route">{c.route}</p>
                  <p className="fd-note">{c.note}</p>
                </div>
              )}
            </div>
          </section>
        </main>

        <footer className="fd-foot">
          Triage and referral support. Not a diagnosis, and not a substitute for a clinician.
        </footer>
      </div>
    </>
  );
}