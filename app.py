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

# ── Client ────────────────────────────────────────────────────────────────────

def get_client():
    try:
        return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    except Exception:
        return anthropic.Anthropic(api_key="YOUR_API_KEY_HERE")


def generate_excuse(client, situation, victim, tone_name, tone_instruction):
    prompt = f"""You are a professional excuse writer.

Situation: {situation}
Sending to: {victim}
Dramatic context: {SITUATIONS[situation]}

{tone_instruction}

Write a 3-4 sentence excuse. NEVER break character.
Treat this like a national emergency.
No humor disclaimers. Just pure dramatic excuse."""

    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        return stream.get_final_text()


def generate_document(client, situation, victim, excuse_text, doc_type):
    doc_prompts = {
        "doctors_note": f"""Create a fake Doctor's Note for this excuse: "{excuse_text}"
Patient missed: {situation} | Sending to: {victim}

Use EXACTLY this format:
DOCTOR NAME: [absurd fake doctor name]
HOSPITAL: [ridiculous fake hospital name]
DIAGNOSIS: [overly technical fake medical diagnosis]
TREATMENT: [absurd treatment plan]
RETURN DATE: [specific future date]
LICENSE #: [fake license number]""",

        "breaking_news": f"""Create a fake Breaking News headline for: "{excuse_text}"
Situation: {situation}

Use EXACTLY this format:
HEADLINE: [sensational all-caps headline]
SUBHEADLINE: [dramatic subheadline]
REPORTER: [fake reporter name]
LOCATION: [fake location]
TIMESTAMP: [date and time]
CHANNEL: [fake news channel name]""",

        "police_report": f"""Create a fake Police Incident Report for: "{excuse_text}"
Situation: {situation}

Use EXACTLY this format:
CASE #: [fake case number]
OFFICER: [fake officer name and badge]
INCIDENT TYPE: [absurd incident classification]
DESCRIPTION: [dramatic 2-sentence description]
LOCATION: [fake location]
RESOLUTION: [absurd resolution status]""",

        "gov_memo": f"""Create a fake Government Memo authorizing this excuse: "{excuse_text}"
Situation: {situation} | Recipient: {victim}

Use EXACTLY this format:
DEPARTMENT: [fake absurd government department]
MEMO #: [fake memo number]
SUBJECT: [dramatic subject line]
BODY: [2-sentence official statement]
CLASSIFICATION: [fake classification level]
SIGNATORY: [fake official name and title]""",
    }

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[{"role": "user", "content": doc_prompts[doc_type]}],
    )
    return response.content[0].text


def generate_roast(client, situation, excuse_text, tone_name):
    prompt = f"""You are a savage AI judge. Rate this excuse and roast it brutally.

Situation: {situation}
Excuse: "{excuse_text}"
Tone used: {tone_name}

Give a score out of 10 for believability and one brutal sentence verdict.
Format: SCORE: X/10 | VERDICT: [one savage sentence]"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


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

if generate_btn:
    if not victim:
        st.error("Enter who you're sending this to.")
        st.stop()

    client = get_client()
    doc_type = DOC_TYPES[doc_type_label]
    tone_instruction = TONES[tone_name] + " " + CHAOS_BOOST[intensity]

    with st.spinner("Crafting your excuse..."):
        excuse_text = generate_excuse(client, situation, victim, tone_name, tone_instruction)
        time.sleep(0.3)

    with st.spinner("Forging your document..."):
        doc_content = generate_document(client, situation, victim, excuse_text, doc_type)
        time.sleep(0.3)

    with st.spinner("AI judge is reviewing..."):
        roast_text = generate_roast(client, situation, excuse_text, tone_name)

    st.divider()
    st.subheader("Your Excuse")
    st.write(f'"{excuse_text}"')

    st.subheader(f"Official Document")
    st.code(doc_content)

    st.subheader("AI Judge's Verdict")
    st.error(roast_text)
