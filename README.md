# 🚀 2026 AI Desktop Assistant (Amit Edition)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge&logo=google-gemini&logoColor=white" alt="Gemini" />
  <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge" alt="Maintained" />
</p>

A powerful, multi-threaded desktop assistant built for **Full-Stack Developers**. It automates your workflow, performs intelligent web research, and looks after your well-being using facial recognition.

---

## 🌟 Key Features

- **🔍 Smart Web Research**: Powered by DuckDuckGo and Gemini AI for instant, clean summaries.
- **🕒 Fatigue Monitor**: Background thread monitors your facial expressions every 5 mins.
- **🎙️ Thread-Safe Voice**: Sophisticated speech engine that handles concurrent audio tasks.
- **📝 Screen Analysis**: Analyzes your active window and generates structured Word docs.
- **🔄 System Reset**: One-key reset for fatigue counters and memory.

---

## 📂 Project Structure

```text
desktop_assistant/
├── main.py              # 🎮 Master Controller & Hotkey Listener
├── vision_module.py      # 👁️ Computer Vision & AI Logic
├── voice_module.py       # 🔊 Speech Engine (TTS/STT)
├── doc_module.py         # 📄 Document Automation
├── personal_info.txt     # 👤 AI Context & Resume Data
└── contacts.csv          # 📱 WhatsApp Contact List
```
---

## 🎮 How to Use
```
Hotkey,   Action,                Result
G,      Web Search,      Listen for query → Search DDG → AI Summarizes & Speaks.
E,      Manual Check,    Instant facial analysis & mood detection.
R,      Reset,           Clears counters and refreshes the assistant state.
V,      Voice Chat,      Deep conversation based on your personal context.

```

---

## 🛠️ Installation & Setup

```
pip install keyboard pyautogui pyttsx3 SpeechRecognition opencv-python \
deepface duckduckgo-search AppOpener python-docx google-generativeai
```
