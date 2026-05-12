# ⚖️ Legal Literacy Bridge

**Legal Literacy Bridge** is a professional AI-powered application designed to break down legal barriers for Ugandan citizens. The app transforms complex legal jargon whether provided as text or via voice recordings into simplified, understandable summaries in local Ugandan languages. It bridges the gap between the formal justice system and the average citizen by providing accessible, narrated legal information in their native tongue.

---

## 🏗️ Architecture Overview

The application follows a modular 4-Phase pipeline using **Sunbird AI** specialized endpoints:

1.  **Input Phase**: User provides typed legal text or uploads an audio file (MP3, WAV, OGG, M4A).
2.  **Phase 1 — Transcription (STT)**: 
    - Audio is normalized and filtered for clarity.
    - Large files are processed using parallel chunking.
    - **API**: Sunbird STT (`/tasks/stt`)
3.  **Phase 2 — Simplification (LLM)**: 
    - The legal text is analyzed and converted into "Plain English" at a primary school comprehension level.
    - **API**: Sunbird Sunflower LLM (`/tasks/sunflower_inference`)
4.  **Phase 3 — Translation (LLM)**: 
    - The simplified summary is translated into Luganda, Runyankole, Ateso, Lugbara, or Acholi.
    - **API**: Sunbird Sunflower LLM (`/tasks/sunflower_inference`)
5.  **Phase 4 — Narration (TTS)**: 
    - The translation is converted into high-quality speech for accessibility.
    - **API**: Sunbird TTS (`/tasks/tts`)

---

## 🛠️ Local Setup

### 1. Prerequisites
- Python 3.9+
- **FFmpeg**: Required for audio processing. 
  - *Windows*: `choco install ffmpeg` 
  - *Linux*: `sudo apt install ffmpeg`

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/Scovia-Barigye/internship-assessment.git
cd internship-assessment/legal_literacy_bridge

# Create and activate virtual environment
python -m venv venv
./venv/Scripts/activate  # Windows
source venv/bin/activate # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the `legal_literacy_bridge` directory based on the provided `.env.example`:
```env
SUNBIRD_API_KEY=your_sunbird_api_key_here
```

### 4. Run the App
```bash
streamlit run app.py
```

---

## 🌍 Environment Variables

| Variable | Description |
| :--- | :--- |
| `SUNBIRD_API_KEY` | Your private API key from the Sunbird AI portal. Required for all AI features. |
| `SUNBIRD_BASE_URL` | (Optional) The base URL for the Sunbird AI API. Defaults to production. |

---

## 📖 Usage Walkthrough

1.  **Select Mode**: Choose between "Paste Legal Text" or "Upload Audio".
2.  **Choose Language**: Select your target Ugandan language from the sidebar.
3.  **Process**: Click the "Analyse" button.
4.  **Review Results**:
    - Expand the **Plain English Summary** to see the simplified version.
    - View the **Translation** in your chosen local language.
    - Use the **Audio Player** to listen to the narration.
5.  **Download**: Use the provided buttons to save the summary or audio for offline use.

---

## 🚀 Deployed Application
Reviewers can try the live application end-to-end here:
👉 [**Legal Literacy Bridge on Hugging Face Spaces**](https://huggingface.co/spaces/barigye05/legal-literacy-bridge)

---

## ⚠️ Known Limitations
- **Audio Clarity**: Extreme background noise may impact transcription accuracy.
- **5-Minute Audio Request**: While the app supports long-form chunking, it is optimized for recordings under 5 minutes per the assessment requirements.
- **Character Limit**: Input text is truncated at 4,000 characters to ensure optimal LLM performance and response quality.

---

## ⚡ Powered by Sunbird AI
This project utilizes the Sunbird STT, TTS, and Sunflower LLM models as part of the Sunbird AI Internship Assessment.
