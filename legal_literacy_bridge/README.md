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

# ⚖️ Legal Literacy Bridge

Bridging the gap between law and citizens through AI-powered simplification and translation.

## Overview
This application helps Ugandan citizens understand complex legal documents by:
1. **Transcribing** audio recordings (STT).
2. **Simplifying** legal jargon into plain English (LLM).
3. **Translating** the summary into local Ugandan languages (Luganda, Runyankole, Ateso, Lugbara, Acholi).
4. **Narrating** the result in the target language (TTS).

## Deployment Note
This app is designed to be deployed to Hugging Face Spaces. 
**Important:** Ensure you set the `SUNBIRD_API_KEY` secret in your Space settings.
