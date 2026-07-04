![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![AI](https://img.shields.io/badge/AI-Gemini%202.5-orange)
![Speech](https://img.shields.io/badge/Speech-Recognition-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

# 🎙️ Jarvis AI Voice Assistant

A voice-controlled AI assistant built with Python that can open applications, browse websites, answer questions using Google's Gemini AI, provide weather updates, read the latest news headlines, and execute multiple commands from a single voice request.

---

## 🚀 Features

### 🎤 Voice Activation

* Wake word: **"Jarvis"**
* Continuous listening mode
* Speak the command directly:

  * `Jarvis open Spotify`
  * `Jarvis what is the weather in Delhi`

---

### 🌐 Open Websites

Jarvis can open popular websites such as:

* Google
* YouTube
* GitHub
* LinkedIn
* Facebook
* Hotstar
* Netflix

Example:

```
Jarvis open Google
```

---

### 💻 Open & Close Applications (macOS)

Supported applications:

* Spotify
* Terminal
* Safari
* Visual Studio Code
* Calculator
* WhatsApp
* Discord
* Finder

Examples:

```
Jarvis open Spotify

Jarvis close Spotify

Jarvis open Terminal
```

Jarvis also checks whether an application is already running before opening it.

---

### 🌦 Weather Information

Get the current weather for any city.

Example:

```
Jarvis weather in Delhi
```

Response includes:

* Temperature
* Feels Like Temperature
* Weather Description

Powered by **OpenWeather API**.

---

### 📰 Daily News

Jarvis reads the latest top headlines.

Example:

```
Jarvis news
```

Powered by **NewsAPI**.

---

### 🤖 AI Assistant

Unknown commands are automatically answered using **Google Gemini 2.5 Flash**.

Examples:

```
Jarvis who is Virat Kohli

Jarvis explain recursion

Jarvis write a Python function for binary search
```

Responses are concise and conversational.

---

### 📅 Date & Time

Examples:

```
Jarvis what is the time

Jarvis what is today's date
```

---

### ⚙️ System Commands

Examples:

```
Jarvis stop

Jarvis restart

Jarvis shutdown
```

---

### 🗣 Multiple Commands

Jarvis can execute multiple commands in a single sentence.

Examples:

```
Jarvis open Spotify and Terminal

Jarvis open Google and YouTube

Jarvis close Spotify and Calculator
```

---

## 🛠 Technologies Used

* Python
* SpeechRecognition
* Google Gemini API
* gTTS
* pygame
* OpenWeather API
* NewsAPI
* python-dotenv

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/PooravMSharma/jarvis-ai-voice-assistant.git
```

Move into the project folder:

```bash
cd jarvis-ai-voice-assistant
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```
GEMINI_API_KEY=your_gemini_api_key

WEATHER_API_KEY=your_openweather_api_key

NEWS_API_KEY=your_newsapi_key
```

---

## ▶️ Run

```bash
python main.py
```

---

## 📁 Project Structure

```
jarvis-ai-voice-assistant/
│
├── main.py
├── musiclibrary.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── venv/ (ignored)
```

---

## 🔮 Future Improvements

* Spotify playback control
* Email support
* Calendar & reminders
* File management
* Browser automation
* Memory system
* Smart AI command parsing
* Local LLM support (Ollama)

---

## 👨‍💻 Author

**Poorav Sharma**

GitHub:
https://github.com/PooravMSharma

---

⭐ If you found this project interesting, consider starring the repository.
