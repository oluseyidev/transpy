# 🌾 Language Assistant

**Empowering Rural Farmers in Nigeria Through Real-Time Speech Translation & Interpretation** 

Built with accessibility and impact in mind, Language Assistant aims to enhance agricultural development and policy outreach, reduce miscommunication, and foster inclusive technology-driven growth and interaction with agricultural extension services in **local languages**. This open-source solution supports farmers in remote areas to access critical information about farming techniques, market prices, weather alerts, and government advisories—through voice and text translation.

Repository: https://github.com/oluseyidev/speech-translator

---

## 🚀 Features

- 🎙️ **Speech Recognition**: Converts spoken words into text.
- 🌐 **Translation**: Translates recognized speech into selected local Nigerian languages.
- 🗣️ **Voice Interpretation**: Reads out translated text using text-to-speech.
- 📱 **Mobile-Friendly Interface**: Optimized for use in field environments with simple UI.
- 🔊 **Offline Capability** (coming soon): To work in low-connectivity rural areas.
- 🧠 Powered by OpenAI & other modern language models.


## 🌾 Target Impact

This tool is designed for:
- 🧑🏾‍🌾 **Rural Farmers**: Receive farming advice in languages they understand.
- 👨🏾‍💼 **Extension Officers**: Communicate effectively with diverse communities.
- 🏛️ **Government Agencies**: Scale outreach programs in agriculture.
- 🤝 **NGOs & Agricultural Initiatives**: Leverage AI for community development.
- Support **agricultural development, food security, and inclusion**

---

## 📦 Project Structure

speech-translator/
├── app.py # Main Flask/FastAPI application
├── translator.py # Core translation logic
├── requirements.txt # Project dependencies
├── models/ # Pre-trained speech translation models
├── static/ or templates/ # (Optional) frontend assets for web UI
└── README.md # Project documentation

## 🚀 Core Features

- 🗣️ **Speech-to-Text (STT):** Convert farmer’s spoken words into text
- 🔤 **Language Translation:** Translate between English and local languages
- 🔉 **Text-to-Speech (TTS):** Voice playback of translated text
- 💬 **Dual-mode interface:** Supports both voice and text input
- 🌐 **Local language support:** Key Nigerian languages such as Hausa, Yoruba, Igbo & Pidgin

---

## 🛠️ Technologies & Dependencies

- **Python 3.8+**  
- **Flask** or **FastAPI** for backend API  
- **deep-translator** or other translation API (Google Translate, LibreTranslate)  
- **Speech recognition libraries**: OpenAI Whisper, Vosk, or Google STT  
- **TTS engine**: gTTS, pyttsx3, or responsive-voice  
- Optionally deployable as a **web or mobile-friendly PWA**

---

## 🧪 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/oluseyidev/speech-translator.git
   cd speech-translator

   Install Python dependencies:

pip install -r requirements.txt
Run the app:

python app.py
Access via terminal prompts or http://localhost:8000 (if a web UI is included)

🎙️ Usage Examples
CLI Mode

python translator.py
Choose source language (e.g., ha for Hausa)

Speak into microphone or enter text

Choose target language (e.g., en for English)

Receive translation as spoken and written output

Web Mode (if available)
Visit localhost:8000

Use voice zones for input/output

Manage translations in languages of your choice

🌾 Agricultural Use Case
Scenario:
A farmer in rural Sokoto receives instructions from an extension officer in English. Using Speech Translator, the farmer can listen to those instructions in Hausa, ask follow-up questions in Hausa, and have their queries translated back into English — fostering better understanding and participation in farming programs.

➕ Future Enhancements
Add offline phrase caching for poor connectivity zones

Expand support to additional Nigerian languages and dialects

Develop mobile-first web UI or a standalone mobile app

Store frequently used phrases, market terms, or agricultural suggestions

Enable multi-user chat mode for live two-way translation

📂 Contributing
We welcome contributions such as:

Adding new languages

Improving accuracy of speech translation

Enhancing UI/UX for users with low digital literacy

To contribute:

Fork this repository

Create your feature branch (git checkout -b my-feature)

Commit your changes and push

Submit a pull request

📜 License
Open-source under the MIT License. Refer to LICENSE for full terms.

📣 Author
Oluseyi Samuel Olalere
3MTT Software Development Knowledge Showcase
GitHub: oluseyidev
