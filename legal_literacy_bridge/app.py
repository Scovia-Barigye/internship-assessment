import streamlit as st
import os
import sys
from pipeline import LegalBridgePipeline
from utils import validate_audio_file, format_error
from sunbird_client import SUPPORTED_LANGUAGES

# Ensure local directory is in PATH for FFmpeg detection if binaries were downloaded locally
sys.path.append(os.getcwd())
if os.path.exists("ffmpeg.exe"):
    os.environ["PATH"] += os.pathsep + os.getcwd()

# 1. Page Configuration & Performance
st.set_page_config(
    page_title="Legal Literacy Bridge",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Premium Law Firm Design System (CSS)
st.markdown("""
    <style>
    /* Global Styles */
    [data-testid="stAppViewContainer"] {
        background-color: #0F1123;
        color: #FFFFFF;
        font-family: 'Segoe UI', 'Inter', sans-serif;
    }
    
    [data-testid="stHeader"] {
        background: rgba(15, 17, 35, 0.9);
    }
    
    .main .block-container {
        padding-top: 2rem;
    }

    /* Typography */
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1A1D2E;
        border-right: 2px solid #FFD700;
        padding-top: 1rem;
    }
    
    .sidebar-card {
        background: #0D0D1A;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 1px solid #2A2D3E;
    }
    
    .gold-label {
        color: #FFD700 !important;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .sidebar-tagline {
        color: #A0A0B0;
        font-style: italic;
        font-size: 13px;
    }

    /* Main Area Header */
    .header-container {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .gold-line {
        border: none;
        border-bottom: 2px solid #FFD700;
        width: 60px;
        margin: 20px auto;
    }
    
    .subtitle {
        color: #A0A0B0;
        font-size: 16px;
    }

    /* Feature Cards */
    .feature-card {
        background: #1A1D2E;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border-top: 3px solid #FFD700;
        height: 100%;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }

    /* Input Controls */
    .stRadio > div {
        background-color: #1A1D2E;
        padding: 5px;
        border-radius: 30px;
        border: 1px solid #2A2D3E;
    }
    
    div[data-testid="stMarkdownContainer"] > p > label {
        color: #FFD700 !important;
        font-weight: bold;
    }

    /* Input Areas */
    textarea, input {
        background-color: #1A1D2E !important;
        color: #FFFFFF !important;
        border: 1px solid #2A2D3E !important;
        border-radius: 10px !important;
    }
    
    textarea:focus {
        border-color: #FFD700 !important;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #FFD700 !important;
        color: #0F1123 !important;
        font-weight: 900 !important;
        border-radius: 8px !important;
        padding: 14px 32px !important;
        border: none !important;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div.stButton > button:hover {
        background-color: #E6C200 !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }

    /* Results Card / Expander */
    .stExpander {
        background-color: #1A1D2E !important;
        border: 1px solid #2A2D3E !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        margin-bottom: 1.5rem;
    }
    
    .stExpander details summary {
        background-color: #1A1D2E !important;
        color: #FFFFFF !important;
        font-weight: bold;
        font-size: 15px;
        padding: 15px;
        border-radius: 12px;
    }
    
    .stExpander details summary:hover {
        color: #FFD700 !important;
    }
    
    .stExpander details summary svg {
        fill: #FFD700 !important;
    }

    /* Force dark blue text for readability inside cards */
    .stExpander [data-testid="stMarkdownContainer"] p {
        color: #F0F0F0 !important;
        line-height: 1.6;
    }

    /* Download Buttons */
    div.stDownloadButton > button {
        background-color: transparent !important;
        color: #FFD700 !important;
        border: 1px solid #FFD700 !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        padding: 6px 16px !important;
        width: auto !important;
    }
    
    div.stDownloadButton > button:hover {
        background-color: #FFD700 !important;
        color: #0F1123 !important;
    }

    /* Success/Info Boxes */
    div[data-testid="stNotification"] {
        background-color: #1A1D2E !important;
        border-radius: 8px;
        border: none;
    }
    
    div[data-testid="stNotification"][class*="success"] { border-left: 4px solid #00C48C; color: #00C48C; }
    div[data-testid="stNotification"][class*="info"] { border-left: 4px solid #FFD700; color: #FFFFFF; }
    div[data-testid="stNotification"][class*="error"] { border-left: 4px solid #FF4B4B; color: #FF8080; }

    /* Custom success card */
    .success-card {
        background: linear-gradient(135deg, #1A1D2E, #0F1123);
        border-left: 4px solid #00C48C;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Audio Container */
    .audio-card {
        background: #0F1123;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2A2D3E;
    }

    /* How it works badges */
    .step-badge {
        display: inline-block;
        color: #FFD700;
        font-weight: bold;
        margin-right: 8px;
    }
    
    .divider-gold {
        border: none;
        border-top: 1px solid #2A2D3E;
        margin: 16px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Layout
with st.sidebar:
    # Branding Card
    st.markdown("""
        <div class="sidebar-card">
            <h2 style='margin:0; color:white;'>⚖️ Legal Literacy</h2>
            <div class="gold-line" style="margin: 10px 0; width: 40px;"></div>
            <p class="sidebar-tagline">Bridging the gap between law and citizens.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Language Selector
    st.markdown('<p class="gold-label">🌍 SELECT TARGET LANGUAGE</p>', unsafe_allow_html=True)
    target_lang = st.selectbox(
        "Target Language",
        options=list(SUPPORTED_LANGUAGES.keys()),
        index=1, # Default to Luganda
        label_visibility="collapsed"
    )
    
    st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)
    
    # How it Works Card
    st.markdown("""
        <div class="sidebar-card">
            <p style="color:#FFD700; font-weight:bold; margin-bottom:15px;">🛠️ How it works</p>
            <p><span class="step-badge">①</span> <span style="color:white;">Input</span><br><small style="color:#A0A0B0;">Provide text or audio</small></p>
            <p><span class="step-badge">②</span> <span style="color:white;">STT</span><br><small style="color:#A0A0B0;">Audio transcription</small></p>
            <p><span class="step-badge">③</span> <span style="color:white;">Simplify</span><br><small style="color:#A0A0B0;">Jargon removal</small></p>
            <p><span class="step-badge">④</span> <span style="color:white;">Translate</span><br><small style="color:#A0A0B0;">Local language</small></p>
            <p><span class="step-badge">⑤</span> <span style="color:white;">Narrate</span><br><small style="color:#A0A0B0;">Audio feedback</small></p>
        </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br><p style='text-align:center; color:#606070; font-size:11px;'>⚡ Powered by Sunbird AI</p>", unsafe_allow_html=True)

# 4. Main Area Header
st.markdown("""
    <div class="header-container">
        <h1>⚖️ Legal Literacy Bridge</h1>
        <p class="subtitle">Breaking down legal barriers for every Ugandan citizen</p>
        <div class="gold-line"></div>
    </div>
""", unsafe_allow_html=True)

# 5. Feature Strip
fcol1, fcol2, fcol3 = st.columns(3)
with fcol1:
    st.markdown('<div class="feature-card"><div class="feature-icon">🎙️</div><b>Speech to Text</b><br><small style="color:#A0A0B0;">Audio transcription in seconds</small></div>', unsafe_allow_html=True)
with fcol2:
    st.markdown('<div class="feature-card"><div class="feature-icon">📖</div><b>Plain English</b><br><small style="color:#A0A0B0;">Legal jargon simplified</small></div>', unsafe_allow_html=True)
with fcol3:
    st.markdown('<div class="feature-card"><div class="feature-icon">🌍</div><b>5 Languages</b><br><small style="color:#A0A0B0;">Luganda · Runyankole · Ateso · Lugbara · Acholi</small></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. Session State Initialization
if "text_result" not in st.session_state:
    st.session_state["text_result"] = None
if "audio_result" not in st.session_state:
    st.session_state["audio_result"] = None

# 7. Input Mode Selection
st.markdown('<p class="gold-label">SELECT INPUT MODE</p>', unsafe_allow_html=True)
input_mode = st.radio(
    "Input Method Selection",
    ["📝 Paste Legal Text", "🎙️ Upload Audio Recording"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

# 8. Main Logic & Display
error_occurred = False

if input_mode == "📝 Paste Legal Text":
    st.markdown('<p class="gold-label">📄 LEGAL TEXT</p>', unsafe_allow_html=True)
    legal_text = st.text_area(
        "Legal Text Input", 
        placeholder="Paste your legal document, contract clause, court notice, or any legal text here...",
        height=200,
        label_visibility="collapsed"
    )
    
    if st.button("🔍 Analyse & Translate", type="primary"):
        if not legal_text.strip():
            st.warning("Please provide some text to analyse.")
        else:
            with st.spinner("⚖️ Processing through 4 AI phases..."):
                try:
                    pipeline = LegalBridgePipeline()
                    st.session_state["text_result"] = pipeline.run_from_text(legal_text, target_lang)
                except EnvironmentError as ee:
                    st.error(f"Setup Error: {str(ee)}")
                    error_occurred = True
                except Exception as e:
                    st.error(format_error(e))
                    error_occurred = True

    # Display Text Results
    if st.session_state["text_result"]:
        res = st.session_state["text_result"]
        st.markdown('<div class="success-card"><span>✅</span><b>Analysis Complete!</b></div>', unsafe_allow_html=True)
        st.markdown('<p class="gold-label">📊 ANALYSIS RESULTS</p><div class="divider-gold"></div>', unsafe_allow_html=True)
        
        with st.expander("📖 Phase 2 — Plain English Summary", expanded=True):
            st.markdown(res["simplified"])
            st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)
            d1, d2 = st.columns([3,1])
            with d2:
                st.download_button(
                    label="Download Summary (TXT)",
                    data=res["simplified"],
                    file_name="simplified_legal.txt",
                    mime="text/plain",
                    key="dl_text_summary"
                )
            
        with st.expander(f"🌍 Phase 3 — {res['target_language']} Translation", expanded=True):
            st.markdown(res["translated"])
            st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)
            d1, d2 = st.columns([3,1])
            with d2:
                st.download_button(
                    label=f"Download {res['target_language']} Translation (TXT)",
                    data=res["translated"],
                    file_name=f"translation_{res['target_language'].lower()}.txt",
                    mime="text/plain",
                    key="dl_text_trans"
                )
            
        with st.expander("🔊 Phase 4 — Audio Narration", expanded=True):
            st.markdown('<p class="gold-label">🔊 LISTEN TO TRANSLATION</p>', unsafe_allow_html=True)
            st.markdown('<div class="audio-card">', unsafe_allow_html=True)
            st.audio(res["audio_bytes"])
            st.markdown('</div><div class="divider-gold"></div>', unsafe_allow_html=True)
            d1, d2 = st.columns([3,1])
            with d2:
                st.download_button(
                    label=f"Download Narration (WAV)",
                    data=res["audio_bytes"],
                    file_name=f"narration_{res['target_language'].lower()}.wav",
                    mime="audio/wav",
                    key="dl_text_audio"
                )

else:
    # Audio Mode
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown('<p class="gold-label">🎙️ AUDIO LANGUAGE (SOURCE)</p>', unsafe_allow_html=True)
        source_lang = st.selectbox(
            "Source Lang",
            options=list(SUPPORTED_LANGUAGES.keys()),
            index=0,
            label_visibility="collapsed"
        )
    
    st.markdown('<p class="gold-label">🎙️ AUDIO FILE</p>', unsafe_allow_html=True)
    uploaded_audio = st.file_uploader(
        "Upload Legal Audio Recording", 
        type=["mp3", "wav", "ogg", "m4a"],
        label_visibility="collapsed"
    )
    st.info("Audio limit: 5 minutes. Supports MP3, WAV, OGG, M4A.")
    
    if st.button("🔍 Transcribe, Analyse & Translate", type="primary"):
        if uploaded_audio is None:
            st.warning("Please upload an audio file first.")
        else:
            with st.spinner("⚖️ Processing through 4 AI phases..."):
                try:
                    audio_bytes, fmt = validate_audio_file(uploaded_audio)
                    pipeline = LegalBridgePipeline()
                    st.session_state["audio_result"] = pipeline.run_from_audio(
                        audio_bytes, fmt, target_lang, 
                        source_lang=source_lang
                    )
                except EnvironmentError as ee:
                    st.error(f"Setup Error: {str(ee)}")
                    error_occurred = True
                except ValueError as ve:
                    st.warning(f"💡 Tip: {str(ve)}")
                    error_occurred = True
                except Exception as e:
                    st.error(format_error(e))
                    error_occurred = True

    # Display Audio Results
    if st.session_state["audio_result"]:
        res = st.session_state["audio_result"]
        st.markdown('<div class="success-card"><span>✅</span><b>Analysis Complete!</b></div>', unsafe_allow_html=True)
        st.markdown('<p class="gold-label">📊 ANALYSIS RESULTS</p><div class="divider-gold"></div>', unsafe_allow_html=True)
        
        with st.expander("📋 Phase 1 — Transcript", expanded=True):
            st.text_area("Original Transcript", value=res["transcript"], height=150, disabled=True)
            
        with st.expander("📖 Phase 2 — Plain English Summary", expanded=True):
            st.markdown(res["simplified"])
            st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)
            d1, d2 = st.columns([3,1])
            with d2:
                st.download_button(
                    label="Download Summary (TXT)",
                    data=res["simplified"],
                    file_name="simplified_audio.txt",
                    mime="text/plain",
                    key="dl_audio_summary"
                )
            
        with st.expander(f"🌍 Phase 3 — {res['target_language']} Translation", expanded=True):
            st.markdown(res["translated"])
            st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)
            d1, d2 = st.columns([3,1])
            with d2:
                st.download_button(
                    label=f"Download {res['target_language']} Translation (TXT)",
                    data=res["translated"],
                    file_name=f"audio_translation_{res['target_language'].lower()}.txt",
                    mime="text/plain",
                    key="dl_audio_trans"
                )
            
        with st.expander("🔊 Phase 4 — Audio Narration", expanded=True):
            st.markdown('<p class="gold-label">🔊 LISTEN TO TRANSLATION</p>', unsafe_allow_html=True)
            st.markdown('<div class="audio-card">', unsafe_allow_html=True)
            st.audio(res["audio_bytes"])
            st.markdown('</div><div class="divider-gold"></div>', unsafe_allow_html=True)
            d1, d2 = st.columns([3,1])
            with d2:
                st.download_button(
                    label=f"Download Narration (WAV)",
                    data=res["audio_bytes"],
                    file_name=f"audio_narration_{res['target_language'].lower()}.wav",
                    mime="audio/wav",
                    key="dl_audio_audio"
                )
