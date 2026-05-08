import streamlit as st
from translator import translate_text
from speech import speech_to_text, generate_audio
from languages import languages

st.set_page_config(
    page_title="Lingua — AI Translator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Page background ── */
.stApp {
    background: #0c0e14;
    color: #e8e4dc;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #111318 !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * {
    color: #c8c4bc !important;
}
[data-testid="stSidebar"] .stSelectbox label {
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #666 !important;
    margin-bottom: 6px;
}

/* ── Sidebar logo area ── */
.sidebar-brand {
    padding: 32px 24px 28px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 24px;
}
.sidebar-brand .wordmark {
    font-family: 'DM Serif Display', serif;
    font-size: 26px;
    color: #e8e4dc;
    letter-spacing: -0.02em;
    line-height: 1;
}
.sidebar-brand .tagline {
    font-size: 11px;
    color: #555;
    margin-top: 5px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Nav pills in sidebar ── */
.nav-label {
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #444 !important;
    padding: 0 0 10px;
    font-weight: 500;
}

/* ── Main content area ── */
.main .block-container {
    max-width: 900px;
    padding: 48px 40px 80px;
}

/* ── Page heading ── */
.page-heading {
    margin-bottom: 36px;
}
.page-heading h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 42px;
    color: #e8e4dc;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin: 0 0 8px;
}
.page-heading p {
    font-size: 15px;
    color: #666;
    margin: 0;
    font-weight: 300;
}

/* ── Accent line ── */
.accent-rule {
    width: 36px;
    height: 2px;
    background: linear-gradient(90deg, #c9a96e, #e8c98a);
    border-radius: 2px;
    margin: 14px 0 20px;
}

/* ── Cards ── */
.card {
    background: #13151c;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 28px 30px;
    margin-bottom: 20px;
}
.card-title {
    font-size: 11px;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: #555;
    margin-bottom: 14px;
    font-weight: 500;
}

/* ── Text inputs ── */
.stTextArea textarea {
    background: #0c0e14 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 16px !important;
    font-weight: 300 !important;
    padding: 16px !important;
    line-height: 1.65 !important;
    resize: vertical !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: rgba(201,169,110,0.5) !important;
    box-shadow: 0 0 0 3px rgba(201,169,110,0.08) !important;
}
.stTextArea textarea::placeholder {
    color: #444 !important;
}
.stTextArea label {
    display: none !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #0c0e14 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8e4dc !important;
}
.stSelectbox > div > div:hover {
    border-color: rgba(201,169,110,0.4) !important;
}
[data-testid="stSelectboxVirtualDropdown"] {
    background: #1a1d26 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}

/* ── Primary button ── */
.stButton > button {
    background: linear-gradient(135deg, #c9a96e 0%, #e8c98a 100%) !important;
    color: #0c0e14 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 13px 32px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(201,169,110,0.25) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Result box ── */
.result-box {
    background: #0c0e14;
    border: 1px solid rgba(201,169,110,0.2);
    border-left: 3px solid #c9a96e;
    border-radius: 10px;
    padding: 20px 22px;
    margin-top: 8px;
    font-size: 17px;
    font-weight: 300;
    line-height: 1.7;
    color: #e8e4dc;
}

/* ── Info chip ── */
.chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(201,169,110,0.1);
    border: 1px solid rgba(201,169,110,0.2);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    color: #c9a96e;
    margin-bottom: 16px;
    font-weight: 500;
}

/* ── Audio player ── */
audio {
    width: 100% !important;
    border-radius: 8px !important;
    margin-top: 10px !important;
}

/* ── Divider ── */
hr {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 24px 0;
}

/* ── Mode badge ── */
.mode-badge {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 32px;
}
.mode-dot {
    width: 8px;
    height: 8px;
    background: #c9a96e;
    border-radius: 50%;
    box-shadow: 0 0 8px rgba(201,169,110,0.6);
}
.mode-name {
    font-size: 13px;
    color: #888;
    letter-spacing: 0.06em;
}

/* ── Two column layout ── */
.col-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

/* ── Spinner override ── */
.stSpinner > div {
    border-top-color: #c9a96e !important;
}

/* ── Subheader overrides ── */
h2, h3, .stSubheader {
    color: #e8e4dc !important;
    font-family: 'DM Serif Display', serif !important;
}

/* ── Select label ── */
.stSelectbox label {
    font-size: 11px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #555 !important;
    font-weight: 500 !important;
}

/* ── Scroll bar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0c0e14; }
::-webkit-scrollbar-thumb { background: #2a2d38; border-radius: 4px; }

</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="wordmark">Lingua</div>
        <div class="tagline">AI Translation Suite</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-label">Mode</div>', unsafe_allow_html=True)

    mode = st.selectbox(
        "Mode",
        ["Text Translation", "Speech To Text", "Speech To Speech"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='margin:28px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:11px; color:#3a3d48; line-height:1.7; padding: 0 4px;">
        Powered by AI language models.<br>
        Supports 50+ languages with<br>
        real-time audio output.
    </div>
    """, unsafe_allow_html=True)

# ── Main content ──────────────────────────────────────────────────────

mode_icons = {
    "Text Translation": "Type & translate",
    "Speech To Text": "Speak to transcribe",
    "Speech To Speech": "Speak & translate"
}

st.markdown(f"""
<div class="page-heading">
    <h1>{mode}</h1>
    <div class="accent-rule"></div>
    <p>{mode_icons.get(mode, "")}</p>
</div>
""", unsafe_allow_html=True)

# ── TEXT TRANSLATION ─────────────────────────────────────────────────
if mode == "Text Translation":

    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown('<div class="card-title">Source text</div>', unsafe_allow_html=True)
        text = st.text_area(
            "Source",
            height=200,
            placeholder="Paste or type the text you'd like to translate…",
            label_visibility="collapsed"
        )

    with col2:
        st.markdown('<div class="card-title">Target language</div>', unsafe_allow_html=True)
        target = st.selectbox(
            "Translate To",
            list(languages.keys()),
            label_visibility="collapsed"
        )
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        translate_btn = st.button("Translate →", key="translate_btn")

    if translate_btn:
        if text.strip():
            with st.spinner("Translating…"):
                translated = translate_text(text, languages[target])

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(f'<div class="chip">✦ {target}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">{translated}</div>', unsafe_allow_html=True)

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="card-title">Audio playback</div>', unsafe_allow_html=True)
            with st.spinner("Generating audio…"):
                audio = generate_audio(translated, languages[target])
            st.audio(audio)
        else:
            st.warning("Please enter some text before translating.")

# ── SPEECH TO TEXT ────────────────────────────────────────────────────
elif mode == "Speech To Text":

    st.markdown("""
    <div style="background:#13151c; border:1px solid rgba(255,255,255,0.07);
                border-radius:16px; padding:32px; text-align:center; margin-bottom:24px;">
        <div style="font-size:48px; margin-bottom:16px; opacity:0.6">🎙</div>
        <div style="font-size:15px; color:#888; font-weight:300; margin-bottom:24px;">
            Click the button below, then speak clearly.<br>
            Your speech will be transcribed in real time.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Start Recording", key="record_stt"):
        with st.spinner("Listening…"):
            text = speech_to_text()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="chip">✦ Transcription</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box">{text}</div>', unsafe_allow_html=True)

# ── SPEECH TO SPEECH ──────────────────────────────────────────────────
elif mode == "Speech To Speech":

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="card-title">Target language</div>', unsafe_allow_html=True)
        target = st.selectbox(
            "Translate To",
            list(languages.keys()),
            label_visibility="collapsed"
        )

    with col2:
        st.markdown('<div class="card-title">Action</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        record_btn = st.button("Record & Translate →", key="record_sts")

    if record_btn:
        with st.spinner("Listening…"):
            text = speech_to_text()

        with st.spinner("Translating…"):
            translated = translate_text(text, languages[target])

        st.markdown("<hr>", unsafe_allow_html=True)

        r1, r2 = st.columns(2, gap="large")

        with r1:
            st.markdown('<div class="chip">✦ You said</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">{text}</div>', unsafe_allow_html=True)

        with r2:
            st.markdown(f'<div class="chip">✦ {target}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-box">{translated}</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="card-title">Audio playback</div>', unsafe_allow_html=True)
        with st.spinner("Generating audio…"):
            audio = generate_audio(translated, languages[target])
        st.audio(audio)