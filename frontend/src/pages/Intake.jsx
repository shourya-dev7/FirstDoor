import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  AGE_OPTIONS,
  DURATION_OPTIONS,
  NONE_OF_THESE,
  RED_FLAGS,
  SEVERITY_OPTIONS,
  computeTriage,
} from "../lib/placeholderTriage";
import {
  INSTRUMENTS,
  INSTRUMENT_ROUTING_OPTIONS,
  INSTRUMENT_ROUTING_QUESTION,
  RESPONSE_SCALE,
  scoreScreening,
} from "../lib/screeningInstruments";

const TRACK_OPTIONS = [
  { id: "emotional", label: "Mainly how I am feeling emotionally" },
  { id: "physical", label: "Mainly a physical symptom" },
];

export default function Intake() {
  const navigate = useNavigate();

  // Which branch of the flow to run. The free-text field is never inspected to
  // decide this — keyword matching on a symptom description is fragile and
  // would route people wrongly. Only this answer decides.
  const [track, setTrack] = useState("");

  const [symptom, setSymptom] = useState("");
  const [ageBand, setAgeBand] = useState("");

  // Physical path only.
  const [duration, setDuration] = useState("");
  const [severity, setSeverity] = useState("");
  const [redFlags, setRedFlags] = useState([]);
  const [noneChecked, setNoneChecked] = useState(false);

  // Emotional path only.
  const [instrument, setInstrument] = useState("");
  const [responses, setResponses] = useState({});

  const isPhysical = track === "physical";
  const isEmotional = track === "emotional";
  const spec = isEmotional && instrument ? INSTRUMENTS[instrument] : null;

  // "None of these apply" and the five warning signs are mutually exclusive.
  function toggleFlag(id) {
    setNoneChecked(false);
    setRedFlags((current) =>
      current.includes(id) ? current.filter((f) => f !== id) : [...current, id]
    );
  }

  function toggleNone() {
    setNoneChecked((current) => !current);
    setRedFlags([]);
  }

  function setResponse(itemId, value) {
    setResponses((current) => ({ ...current, [itemId]: value }));
  }

  // Switching instruments clears answers so responses can never be carried
  // from one questionnaire's items to another's.
  function chooseInstrument(id) {
    setInstrument(id);
    setResponses({});
  }

  let answered = [];
  if (isPhysical) {
    answered = [
      symptom.trim() !== "",
      duration !== "",
      severity !== "",
      ageBand !== "",
      redFlags.length > 0 || noneChecked,
    ];
  } else if (isEmotional) {
    answered = [
      instrument !== "",
      symptom.trim() !== "",
      ageBand !== "",
      spec ? spec.items.every((item) => responses[item.id] !== undefined) : false,
    ];
  }

  const remaining = answered.filter((a) => !a).length;
  const ready = track !== "" && remaining === 0;

  function handleSubmit(event) {
    event.preventDefault();
    if (!ready) return;

    const result = isPhysical
      ? computeTriage({ symptom, duration, severity, ageBand, redFlags })
      : scoreScreening({
          instrument,
          responses,
          symptom,
          ageBandLabel: AGE_OPTIONS.find((o) => o.id === ageBand)?.label ?? "",
        });

    navigate("/result", { state: { result } });
  }

  function choice(name, options, value, setValue) {
    return (
      <div className="in-opts">
        {options.map((o) => (
          <label className="in-opt" key={o.id}>
            <input
              type="radio"
              name={name}
              value={o.id}
              checked={value === o.id}
              onChange={() => setValue(o.id)}
            />
            <span>{o.label}</span>
          </label>
        ))}
      </div>
    );
  }

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #06262E; }
        .in { min-height: 100vh; background: #06262E; color: #EAF4F5;
              font-family: 'IBM Plex Sans', system-ui, sans-serif; }
        .in-bar { display: flex; justify-content: space-between; align-items: center;
                  padding: 20px 6vw; border-bottom: 1px solid #12414C; }
        .in-mark { display: inline-block; font-family: 'Instrument Serif', serif; font-size: 28px;
                   color: inherit; text-decoration: none; border-radius: 4px; }
        .in-mark span { color: #02C39A; }
        .in-mark:hover { color: #02C39A; }
        .in-mark:focus-visible { outline: 2px solid #02C39A; outline-offset: 3px; }
        .in-step { font-size: 11.5px; letter-spacing: .14em; text-transform: uppercase; color: #6E959E; }
        .in-wrap { max-width: 780px; margin: 0 auto; padding: 6vh 5vw 10vh; }
        .in-intro { margin-bottom: 26px; }
        .in-h1 { font-family: 'Instrument Serif', serif; font-weight: 400;
                 font-size: clamp(32px, 4.4vw, 46px); line-height: 1.08; letter-spacing: -.015em; }
        .in-h1 em { font-style: italic; color: #02C39A; }
        .in-sub { margin-top: 14px; font-size: 16px; line-height: 1.6; color: #9FC9CE; max-width: 52ch; }
        .in-card { background: #F4F1E9; color: #123038; border-radius: 14px;
                   padding: 34px; box-shadow: 0 24px 60px rgba(0,0,0,.34); }
        .in-q { border: none; padding: 0; margin: 0 0 30px; }
        .in-q:last-of-type { margin-bottom: 0; }
        .in-legend { display: flex; align-items: baseline; gap: 11px; font-size: 18px;
                     font-weight: 600; line-height: 1.35; padding: 0; }
        .in-num { font-family: 'Instrument Serif', serif; font-size: 25px; font-weight: 400;
                  color: #B6AE99; line-height: 1; width: 22px; flex-shrink: 0; }
        .in-help { font-size: 14px; color: #6F7E7E; line-height: 1.55; margin: 7px 0 0 33px; }
        .in-body { margin: 14px 0 0 33px; }
        .in-text { width: 100%; min-height: 118px; resize: vertical; font: inherit; font-size: 15.5px;
                   line-height: 1.6; color: #123038; background: #FBFAF6; border: 1px solid #DAD4C4;
                   border-radius: 9px; padding: 13px 14px; }
        .in-text::placeholder { color: #A3ADAB; }
        .in-text:focus-visible { outline: 2px solid #02C39A; outline-offset: 1px; border-color: #02C39A; }
        .in-opts { display: grid; grid-template-columns: 1fr 1fr; gap: 9px; }
        .in-opt { display: flex; align-items: flex-start; gap: 10px; cursor: pointer;
                  background: #FBFAF6; border: 1px solid #DAD4C4; border-radius: 9px;
                  padding: 13px 14px; font-size: 15px; line-height: 1.45; }
        .in-opt:hover { border-color: #B6AE99; }
        .in-opt input { accent-color: #02C39A; width: 17px; height: 17px; margin-top: 1px; flex-shrink: 0; }
        .in-opt input:focus-visible { outline: 2px solid #02C39A; outline-offset: 2px; }
        .in-opt:has(input:checked) { border-color: #02C39A; background: #ECF7F3; }
        .in-opt:focus-within { border-color: #02C39A; }

        .in-flags { background: #FBEAE4; border: 1px solid #E0AF9E; border-left: 3px solid #B4442C;
                    border-radius: 11px; padding: 22px 24px; margin-top: 34px; }
        .in-flags .in-legend { color: #B4442C; }
        .in-flags .in-num { color: #D08D77; }
        .in-flags .in-help { color: #8A5344; }
        .in-flag-label { font-size: 10.5px; letter-spacing: .16em; text-transform: uppercase;
                         color: #B4442C; font-weight: 600; margin-bottom: 12px; }
        .in-flag-list { display: grid; gap: 8px; margin: 14px 0 0 33px; }
        .in-flag { display: flex; align-items: flex-start; gap: 10px; cursor: pointer;
                   background: #FDF4F1; border: 1px solid #E7C4B7; border-radius: 9px;
                   padding: 13px 14px; font-size: 15px; line-height: 1.45; }
        .in-flag:hover { border-color: #D08D77; }
        .in-flag input { accent-color: #B4442C; width: 17px; height: 17px; margin-top: 1px; flex-shrink: 0; }
        .in-flag input:focus-visible { outline: 2px solid #B4442C; outline-offset: 2px; }
        .in-flag:has(input:checked) { border-color: #B4442C; background: #F9E4DD; }
        .in-flag:focus-within { border-color: #B4442C; }
        .in-none { margin-top: 12px; border-style: dashed; }
        .in-none:has(input:checked) { border-style: solid; border-color: #0B6B57;
                                      background: #E6F4EE; }
        .in-none input { accent-color: #0B6B57; }
        .in-none input:focus-visible { outline: 2px solid #0B6B57; }

        .in-notice { background: #FBF2E2; border: 1px solid #DFC894; border-left: 3px solid #8A5A12;
                     border-radius: 11px; padding: 16px 18px; margin: 0 0 26px 33px; }
        .in-notice-label { font-size: 10.5px; letter-spacing: .16em; text-transform: uppercase;
                           color: #8A5A12; font-weight: 600; margin-bottom: 7px; }
        .in-notice p { font-size: 13.5px; line-height: 1.55; color: #6B5424; }
        .in-item { border: none; padding: 18px 0 0; margin: 0; border-top: 1px solid #E6E1D3; }
        .in-item:first-of-type { border-top: none; padding-top: 0; }
        .in-item-legend { display: flex; align-items: baseline; gap: 10px; font-size: 15.5px;
                          font-weight: 500; line-height: 1.45; padding: 0 0 11px; }
        .in-item-n { font-size: 12px; color: #97A3A2; font-variant-numeric: tabular-nums;
                     width: 26px; flex-shrink: 0; }
        .in-scale { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 8px; margin-left: 36px; }
        .in-scale .in-opt { padding: 11px 13px; font-size: 14px; }
        .in-items { margin: 16px 0 0 33px; display: grid; gap: 18px; }

        .in-send { margin-top: 30px; padding-top: 26px; border-top: 1px solid #DAD4C4;
                   display: flex; align-items: center; gap: 18px; flex-wrap: wrap; }
        .in-btn { font: inherit; font-size: 15.5px; font-weight: 600; color: #06262E;
                  background: #02C39A; border: none; border-radius: 9px; padding: 14px 26px;
                  cursor: pointer; }
        .in-btn:hover:not(:disabled) { background: #04D8AB; }
        .in-btn:focus-visible { outline: 2px solid #123038; outline-offset: 3px; }
        .in-btn:disabled { background: #DFDACB; color: #98A09E; cursor: not-allowed; }
        .in-hint { font-size: 13.5px; color: #6F7E7E; line-height: 1.5; }
        .in-warn { margin-top: 22px; font-size: 13.5px; line-height: 1.6; color: #6F7E7E;
                   border-left: 2px solid #DAD4C4; padding-left: 13px; }
        .in-foot { text-align: center; margin-top: 24px; font-size: 12.5px; color: #55808A; }

        @media (max-width: 600px) {
          .in-card { padding: 24px; }
          .in-opts { grid-template-columns: 1fr; }
          .in-scale { grid-template-columns: 1fr; margin-left: 0; }
          .in-help, .in-body, .in-flag-list, .in-items, .in-notice { margin-left: 0; }
          .in-flags { padding: 20px 17px; }
          .in-send { gap: 12px; }
          .in-btn { width: 100%; }
        }
      `}</style>

      <div className="in">
        <header className="in-bar">
          <Link className="in-mark" to="/">First<span>Door</span></Link>
          <div className="in-step">Step 1 of 2 · Intake</div>
        </header>

        <div className="in-wrap">
          <div className="in-intro">
            <h1 className="in-h1">A few questions, then <em>which door</em>.</h1>
            <p className="in-sub">
              Answer in your own words. FirstDoor works out how urgent this is and who should
              look at it — it does not name a condition and it does not suggest a medicine.
            </p>
          </div>

          <form className="in-card" onSubmit={handleSubmit} noValidate>
            <fieldset className="in-q">
              <legend className="in-legend">
                <span className="in-num">1</span>
                What brings you here today?
              </legend>
              <p className="in-help">
                This decides which questions you are asked next.
              </p>
              <div className="in-body">
                {choice("track", TRACK_OPTIONS, track, setTrack)}
              </div>
            </fieldset>

            {isPhysical && (
              <>
                <fieldset className="in-q">
                  <legend className="in-legend">
                    <span className="in-num">2</span>
                    Describe what you are feeling
                  </legend>
                  <p className="in-help">
                    Where it is, what it feels like, and anything that makes it better or worse.
                  </p>
                  <div className="in-body">
                    <textarea
                      className="in-text"
                      value={symptom}
                      onChange={(e) => setSymptom(e.target.value)}
                      placeholder="For example: a dull ache under my ribs that gets worse after eating…"
                    />
                  </div>
                </fieldset>

                <fieldset className="in-q">
                  <legend className="in-legend">
                    <span className="in-num">3</span>
                    How long has this been going on?
                  </legend>
                  <div className="in-body">
                    {choice("duration", DURATION_OPTIONS, duration, setDuration)}
                  </div>
                </fieldset>

                <fieldset className="in-q">
                  <legend className="in-legend">
                    <span className="in-num">4</span>
                    How much is it affecting you?
                  </legend>
                  <div className="in-body">
                    {choice("severity", SEVERITY_OPTIONS, severity, setSeverity)}
                  </div>
                </fieldset>

                <fieldset className="in-q">
                  <legend className="in-legend">
                    <span className="in-num">5</span>
                    Which age band are you in?
                  </legend>
                  <div className="in-body">
                    {choice("ageBand", AGE_OPTIONS, ageBand, setAgeBand)}
                  </div>
                </fieldset>

                <fieldset className="in-q in-flags">
                  <p className="in-flag-label">Check carefully</p>
                  <legend className="in-legend">
                    <span className="in-num">6</span>
                    Is any of this happening right now?
                  </legend>
                  <p className="in-help">
                    Tick everything that applies. Any one of these sends you straight to
                    emergency care.
                  </p>
                  <div className="in-flag-list">
                    {RED_FLAGS.map((flag) => (
                      <label className="in-flag" key={flag.id}>
                        <input
                          type="checkbox"
                          checked={redFlags.includes(flag.id)}
                          onChange={() => toggleFlag(flag.id)}
                        />
                        <span>{flag.label}</span>
                      </label>
                    ))}
                    <label className="in-flag in-none">
                      <input type="checkbox" checked={noneChecked} onChange={toggleNone} />
                      <span>{NONE_OF_THESE.label}</span>
                    </label>
                  </div>
                </fieldset>
              </>
            )}

            {isEmotional && (
              <>
                <fieldset className="in-q">
                  <legend className="in-legend">
                    <span className="in-num">2</span>
                    {INSTRUMENT_ROUTING_QUESTION}
                  </legend>
                  <p className="in-help">
                    This decides which screening questionnaire you are asked.
                  </p>
                  <div className="in-body">
                    {choice("instrument", INSTRUMENT_ROUTING_OPTIONS, instrument, chooseInstrument)}
                  </div>
                </fieldset>

                <fieldset className="in-q">
                  <legend className="in-legend">
                    <span className="in-num">3</span>
                    Describe how you have been feeling
                  </legend>
                  <p className="in-help">
                    In your own words. Nothing here is used to pick your questions.
                  </p>
                  <div className="in-body">
                    <textarea
                      className="in-text"
                      value={symptom}
                      onChange={(e) => setSymptom(e.target.value)}
                      placeholder="Take as much or as little space as you want…"
                    />
                  </div>
                </fieldset>

                <fieldset className="in-q">
                  <legend className="in-legend">
                    <span className="in-num">4</span>
                    Which age band are you in?
                  </legend>
                  <div className="in-body">
                    {choice("ageBand", AGE_OPTIONS, ageBand, setAgeBand)}
                  </div>
                </fieldset>

                {spec && (
                  <fieldset className="in-q">
                    <legend className="in-legend">
                      <span className="in-num">5</span>
                      {spec.name} screening
                    </legend>

                    <div className="in-notice">
                      <p className="in-notice-label">Not yet configured</p>
                      <p>
                        The question wording and response labels below are placeholders. The
                        official {spec.name} wording has to be pasted in from the source
                        instrument before this is shown to anyone.
                      </p>
                    </div>

                    <div className="in-items">
                      {spec.items.map((item, index) => (
                        <fieldset className="in-item" key={item.id}>
                          <legend className="in-item-legend">
                            <span className="in-item-n">
                              {index + 1}/{spec.items.length}
                            </span>
                            {item.text}
                          </legend>
                          <div className="in-scale">
                            {RESPONSE_SCALE.map((option) => (
                              <label className="in-opt" key={option.value}>
                                <input
                                  type="radio"
                                  name={item.id}
                                  value={option.value}
                                  checked={responses[item.id] === option.value}
                                  onChange={() => setResponse(item.id, option.value)}
                                />
                                <span>{option.label}</span>
                              </label>
                            ))}
                          </div>
                        </fieldset>
                      ))}
                    </div>
                  </fieldset>
                )}
              </>
            )}

            <div className="in-send">
              <button
                className="in-btn"
                type="submit"
                disabled={!ready}
                aria-describedby="in-hint"
              >
                See my result
              </button>
              <p className="in-hint" id="in-hint">
                {track === ""
                  ? "Answer the first question to begin."
                  : ready
                    ? "Everything answered."
                    : `${remaining} question${remaining === 1 ? "" : "s"} still to answer.`}
              </p>
            </div>

            <p className="in-warn">
              FirstDoor does not diagnose conditions and does not recommend medication.
              If you think this is an emergency, call your local emergency number now.
            </p>
          </form>

          <p className="in-foot">
            Triage and referral support. Not a diagnosis, and not a substitute for a clinician.
          </p>
        </div>
      </div>
    </>
  );
}
