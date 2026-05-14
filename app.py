import streamlit as st
import anthropic
import time

# ── Data ──────────────────────────────────────────────────────────────────────

SITUATIONS = {
    "💼 Late to work":       "catastrophic morning infrastructure failure",
    "👻 Ghosted someone":    "involuntary communication blackout",
    "🏋️ Missed gym":        "severe physical incapacitation requiring immediate rest",
    "🎂 Forgot birthday":    "acute memory impairment due to critical workload",
    "📱 Ignored texts":      "emergency device malfunction protocol",
    "🍕 Ate their food":     "involuntary sustenance acquisition disorder",
    "😴 Overslept":          "mandatory circadian rhythm recalibration event",
    "📚 Missed deadline":    "force majeure project complexity escalation",
    "✈️ Missed flight":      "unprecedented transportation infrastructure collapse",
    "🎮 Played games all day": "mandatory cognitive decompression therapy session",
}

TONES = {
    "🎩 Professional":        "Use formal corporate language. Treat this like a board meeting.",
    "🏴‍☠️ Pirate Speak":      "Speak entirely like a dramatic pirate. Use 'arr', 'matey', 'blimey' etc.",
    "🎭 Shakespearean":       "Write in full Shakespearean English with thee/thou/hath. Make it tragic.",
    "🕵️ 1920s Noir":         "Write like a cynical 1920s detective monologue. World-weary and dark.",
    "🌐 Conspiracy Theory":   "Write with paranoid conspiracy language. Shadow governments, cover-ups.",
    "🤖 Robot Malfunction":   "Write like an AI having a breakdown. Include ERROR codes and glitches.",
    "👶 Baby Talk":           "Write like a toddler explaining a very serious situation. Lisps welcome.",
    "🔬 Scientist":           "Use overly technical scientific jargon. Cite fake studies and data.",
}

DOC_TYPES = {
    "🏥 Doctor's Note":          "doctors_note",
    "📰 Breaking News":           "breaking_news",
    "🚔 Police Incident Report":  "police_report",
    "🏛️ Government Memo":        "gov_memo",
}

CHAOS_BOOST = {
    "Mild":          "",
    "Unhinged":      "Escalate the drama by 3x. Add unnecessary details.",
    "Maximum Chaos": "Go completely off the rails. This is the most dramatic excuse ever written in human history. Pull no punches.",
}

# ── UI ────────────────────────────────────────────────────────────────────────

st.title("🎭 AI Excuse Generator")
st.caption("Build absurd alibis. Beat accountability.")

col1, col2 = st.columns(2)

with col1:
    situation = st.selectbox("What happened?", list(SITUATIONS.keys()))
    victim = st.text_input("Who are you sending this to?", placeholder="My boss, my partner, my mom...")

with col2:
    tone_name = st.selectbox("Tone", list(TONES.keys()))
    doc_type_label = st.selectbox("Document type", list(DOC_TYPES.keys()))

intensity = st.select_slider(
    "Chaos level",
    options=["Mild", "Unhinged", "Maximum Chaos"],
    value="Unhinged",
)

generate_btn = st.button("🚀 Generate Excuse + Receipt", type="primary", use_container_width=True)
