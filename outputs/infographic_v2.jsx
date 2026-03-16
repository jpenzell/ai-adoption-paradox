import { useState, useEffect } from "react";

const data = {
  features: [
    { label: "How you FEEL about AI",          pct: 41.3, highlight: true  },
    { label: "Whether you use AI agents",       pct: 12.9, highlight: false },
    { label: "Learned a new AI tool this year", pct: 12.9, highlight: false },
    { label: "How much you trust AI",           pct: 10.3, highlight: false },
    { label: "How well AI handles complexity",  pct:  9.5, highlight: false },
    { label: "Years in tech",                   pct:  2.7, highlight: false },
  ],
  archetypes: [
    { name: "Daily Integrators",     sent: "Very Favorable", usage: "Daily",        i: 0 },
    { name: "Enthusiastic Adopters", sent: "Very Favorable",  usage: "Daily–Weekly", i: 1 },
    { name: "Cautious Experimenters",sent: "Neutral",      usage: "Weekly",       i: 2 },
    { name: "Pragmatic Dabblers",    sent: "Favorable",    usage: "Monthly",      i: 3 },
    { name: "Active Resisters",      sent: "Unfavorable",    usage: "Never",        i: 4 },
  ],
};

const ACCENT  = "#E8630A";
const INK     = "#1A1208";
const PAPER   = "#F5F0E8";
const MID     = "#6B5E4E";
const RULE    = "#C8BCA8";
const HILIGHT = "#FFF3E0";

const sentColors = ["#2E7D32","#558B2F","#F9A825","#EF6C00","#C62828"];

export default function App() {
  const [animated, setAnimated] = useState(false);
  useEffect(() => { const t = setTimeout(() => setAnimated(true), 300); return () => clearTimeout(t); }, []);

  return (
    <div style={{ background: "#E8E0D0", minHeight: "100vh", padding: "24px 0", display: "flex", justifyContent: "center" }}>
    <div style={{
      fontFamily: "Georgia, 'Times New Roman', serif",
      background: PAPER,
      width: 680,
      boxShadow: "0 12px 80px rgba(0,0,0,0.22)",
      position: "relative",
      overflow: "hidden",
    }}>

      {/* TOP RULES */}
      <div style={{ height: 5, background: INK }}/>
      <div style={{ height: 3, background: ACCENT, marginTop: 3 }}/>

      {/* HEADER */}
      <div style={{ padding: "32px 48px 0" }}>
        <div style={{ fontSize: 10, letterSpacing: 4, textTransform: "uppercase", color: MID, marginBottom: 14 }}>
          2025 Stack Overflow Developer Survey · n = 33,231
        </div>
        <div style={{ fontSize: 44, fontWeight: "bold", lineHeight: 1.05, color: INK, letterSpacing: -1.5 }}>
          What you <em style={{ color: ACCENT }}>feel</em> about AI<br/>
          predicts whether<br/>
          you use it daily.
        </div>
        <div style={{ marginTop: 14, fontSize: 15, color: MID, lineHeight: 1.55, fontStyle: "italic", maxWidth: 460 }}>
          Not your job title. Not your years of experience.<br/>Not even how much you trust it.
        </div>
      </div>

      {/* HERO STAT */}
      <div style={{ margin: "28px 48px 0", background: INK, padding: "28px 36px", display: "flex", alignItems: "center", gap: 28, position: "relative", overflow: "hidden" }}>
        <div style={{ position: "absolute", top: -40, right: -40, width: 180, height: 180, borderRadius: "50%", background: ACCENT, opacity: 0.1 }}/>
        <div style={{ flexShrink: 0 }}>
          <div style={{ fontSize: 88, fontWeight: "bold", lineHeight: 1, color: ACCENT, letterSpacing: -4 }}>
            41<span style={{ fontSize: 44 }}>.3%</span>
          </div>
          <div style={{ fontSize: 11, color: RULE, letterSpacing: 2, textTransform: "uppercase", marginTop: 2 }}>
            of predictive power
          </div>
        </div>
        <div style={{ borderLeft: `2px solid ${ACCENT}`, paddingLeft: 26 }}>
          <div style={{ fontSize: 15, color: PAPER, lineHeight: 1.55, fontStyle: "italic" }}>
            AI sentiment is the #1 predictor of daily adoption — outweighing trust, experience, role, and learning history combined.
          </div>
          <div style={{ fontSize: 10, color: MID, marginTop: 10, letterSpacing: 1.5, textTransform: "uppercase" }}>
            RF · 200 trees · 77.1% accuracy · 5-fold CV confirmed
          </div>
        </div>
      </div>

      {/* BAR CHART */}
      <div style={{ padding: "28px 48px 0" }}>
        <div style={{ fontSize: 11, letterSpacing: 3, textTransform: "uppercase", color: MID, borderBottom: `1px solid ${RULE}`, paddingBottom: 8, marginBottom: 16 }}>
          What actually predicts daily AI use
        </div>
        {data.features.map((f, i) => (
          <div key={i} style={{ marginBottom: 13, display: "flex", alignItems: "center", gap: 12 }}>
            <div style={{ width: 200, flexShrink: 0 }}>
              <div style={{ fontSize: f.highlight ? 14 : 12, color: f.highlight ? INK : MID, fontWeight: f.highlight ? "bold" : "normal", lineHeight: 1.3 }}>
                {f.label}
              </div>
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ height: f.highlight ? 18 : 11, background: "#E0D8CC", borderRadius: 2, overflow: "hidden" }}>
                <div style={{
                  height: "100%",
                  width: animated ? `${(f.pct / 38) * 100}%` : "0%",
                  background: f.highlight ? ACCENT : MID,
                  opacity: f.highlight ? 1 : 0.45,
                  borderRadius: 2,
                  transition: `width ${0.5 + i * 0.12}s cubic-bezier(0.4,0,0.2,1)`,
                }}/>
              </div>
            </div>
            <div style={{ width: 44, textAlign: "right", flexShrink: 0, fontSize: f.highlight ? 16 : 13, fontWeight: f.highlight ? "bold" : "normal", color: f.highlight ? ACCENT : MID }}>
              {f.pct}%
            </div>
          </div>
        ))}
      </div>

      {/* ARCHETYPE STRIP */}
      <div style={{ padding: "24px 48px 0" }}>
        <div style={{ fontSize: 11, letterSpacing: 3, textTransform: "uppercase", color: MID, borderBottom: `1px solid ${RULE}`, paddingBottom: 8, marginBottom: 14 }}>
          The pattern holds across all five archetypes
        </div>
        <div style={{ display: "flex", gap: 0 }}>
          {data.archetypes.map((a) => (
            <div key={a.i} style={{
              flex: 1, padding: "12px 8px", textAlign: "center",
              borderLeft: a.i === 0 ? `3px solid ${sentColors[a.i]}` : `1px solid ${RULE}`,
              background: a.i === 0 ? `${sentColors[0]}15` : "transparent",
            }}>
              <div style={{ fontSize: 9.5, fontWeight: "bold", color: sentColors[a.i], textTransform: "uppercase", letterSpacing: 0.3, marginBottom: 6, lineHeight: 1.2 }}>
                {a.sent}
              </div>
              <div style={{ fontSize: 10, color: a.i === 0 ? INK : MID, fontStyle: "italic", lineHeight: 1.3, marginBottom: 4 }}>
                {a.name}
              </div>
              <div style={{ fontSize: 9, color: a.i === 0 ? INK : RULE, textTransform: "uppercase", letterSpacing: 0.3 }}>
                {a.usage}
              </div>
            </div>
          ))}
        </div>
        <div style={{ marginTop: 8, fontSize: 11, color: MID, fontStyle: "italic", textAlign: "center" }}>
          Usage frequency decreases left to right; sentiment broadly follows but not strictly.
        </div>
      </div>

      {/* STAT TRIO */}
      <div style={{ padding: "22px 48px 0", display: "flex", gap: 14 }}>
        {[
          { stat: "4×",   desc: "Sentiment outpredicts trust as a driver of daily adoption" },
          { stat: "15×",  desc: "More predictive than years of industry experience" },
          { stat: "29pp", desc: "Trust gap: structured vs. informal AI learners" },
        ].map((c, i) => (
          <div key={i} style={{
            flex: 1, padding: "16px 14px",
            border: `1px solid ${RULE}`,
            borderTop: `3px solid ${i === 0 ? ACCENT : RULE}`,
            background: i === 0 ? HILIGHT : "transparent",
          }}>
            <div style={{ fontSize: 32, fontWeight: "bold", color: ACCENT, lineHeight: 1 }}>{c.stat}</div>
            <div style={{ fontSize: 11, color: MID, marginTop: 6, lineHeight: 1.4 }}>{c.desc}</div>
          </div>
        ))}
      </div>

      {/* PULL QUOTE */}
      <div style={{ margin: "22px 48px 0", borderLeft: `4px solid ${ACCENT}`, padding: "16px 20px", background: `${ACCENT}0A` }}>
        <div style={{ fontSize: 16, color: INK, lineHeight: 1.55, fontStyle: "italic" }}>
          "If you want people to use AI, change how they feel about it first —<br/>not how much they know about it."
        </div>
        <div style={{ fontSize: 11, color: MID, marginTop: 8, letterSpacing: 1, textTransform: "uppercase" }}>
          The implication for L&D and change management
        </div>
      </div>

      {/* FOOTER */}
      <div style={{ margin: "22px 48px 0", paddingTop: 16, borderTop: `1px solid ${RULE}`, display: "flex", justifyContent: "space-between", alignItems: "flex-end", paddingBottom: 32 }}>
        <div>
          <div style={{ fontSize: 13, fontWeight: "bold", color: INK }}>Josh Penzell</div>
          <div style={{ fontSize: 10, color: MID, fontStyle: "italic" }}>Founder, Imagination Applied · AI Transformation Consulting</div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: 10, color: MID }}>Source: 2025 Stack Overflow Developer Survey</div>
          <div style={{ fontSize: 10, color: MID }}>Random Forest · n=33,231 · 77.1% accuracy</div>
        </div>
      </div>

      {/* BOTTOM RULES */}
      <div style={{ height: 3, background: ACCENT }}/>
      <div style={{ height: 5, background: INK }}/>
    </div>
    </div>
  );
}
