---
title: Legal Literacy Bridge
emoji: ⚖️
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
---

This readme is specifically for Hugging Face Spaces.
## 🚀 Deployment on Hugging Face Spaces
This application is hosted on Hugging Face Spaces using the **Streamlit SDK**. 
- **Environment**: The app runs in a containerized Linux environment.
- **System Dependencies**: We use `packages.txt` to ensure `ffmpeg` is installed for high-quality audio processing.
- **Security**: API keys are managed via Hugging Face **Secrets** to keep credentials safe.
