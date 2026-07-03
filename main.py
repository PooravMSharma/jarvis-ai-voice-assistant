import speech_recognition as sr
import webbrowser
import requests
from google import genai
import datetime
from gtts import gTTS
from dotenv import load_dotenv
import subprocess
import tempfile
import pygame
import time
import sys
import os
import re


load_dotenv()

newsapi =  os.getenv("NEWS_API_KEY")


def is_running(app):
    result = subprocess.run(
        ["pgrep", "-x", app],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

is_speaking = False

def speak(text):
    global is_speaking
    is_speaking = True

    fd, filename = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)

    try:
        tts = gTTS(text)
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()

    finally:
        is_speaking = False

        if os.path.exists(filename):
            os.remove(filename)


def ask_ai(command):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""You are Jarvis, my personal AI assistant.

            Keep responses under four short sentences.

            If the user asks coding questions,
            reply clearly and professionally.

            User:
            {command}
            """
    )

    return response.text

weather_api = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        # for debugging
        # print("City =", city)
        # print("Status =", response.status_code)
        # print(data)

        if response.status_code == 200:
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            description = data["weather"][0]["description"]

            return f"{city}: {temp}°C, feels like {feels_like}°C, {description}"

        return "City not found."

    except Exception as e:
        print(e)
        return "Unable to fetch weather."


WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com/PooravMSharma",
    "linkedin": "https://www.linkedin.com",
    "facebook": "https://www.facebook.com",
    "hotstar": "https://www.hotstar.com/in/onboarding/profile?ref=%2Fin%2Fhome",
    "netflix": "https://www.netflix.com/in/"
}

APPS = {
    "spotify": "Spotify",
    "calculator": "Calculator",
    "cloud": "Claude",
    "vs code": "Visual Studio Code",
    "whatsapp": "WhatsApp",
    "discord": "Discord",
    "files": "Finder",
    "safari": "Safari",
    "terminal": "Terminal",
}

def handle_apps_and_websites(c):
    words = c.split(maxsplit=1)

    if len(words) < 2:
        return False

    action = words[0]
    target = words[1].strip()

    if action == "open":

        if target in WEBSITES:
            webbrowser.open(WEBSITES[target])
            return True

        if target in APPS:
            if not is_running(APPS[target]):
                os.system(f'open -a "{APPS[target]}"')
            else:
                speak(f"{target} is already open.")
            return True

    elif action == "close":

        if target in APPS:
            if is_running(APPS[target]):
                os.system(f'''osascript -e 'quit app "{APPS[target]}"' ''')
            else:
                speak(f"{target} is already closed.")
            return True

    return False
        
def handle_news(c):
    if "news" in c:
        speak("Here are today's top headlines.")

        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?language=en&pageSize=5&apiKey={newsapi}"
        )

        if r.status_code == 200:
            data = r.json()

            articles = data.get("articles", [])

            for i, article in enumerate(articles, start=1):
                title = article["title"]
                print(f"{i}. {title}")
                speak(title)
                return True
            
        return False

def handle_information(c):

    if "time" in c:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
        return True

    elif "date" in c:
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today is {current_date}.") 
        return True

    elif "weather in" in c:

        city = c.lower().split("weather in")[-1].strip()

        weather = get_weather(city)

        print(weather)
        speak(weather)
        return True
    
    return False

def handle_system(c):
    if any(x in c for x in [
        "stop talking",
        "stop speaking",
        "be quiet",
        "stop"
    ]):
        pygame.mixer.music.stop()
        return True

    elif "shutdown" in c:
        speak("Goodbye boss")
        exit()

    elif "restart" in c:
        speak("Restarting")

        os.execl(sys.executable, sys.executable, *sys.argv)
    
    return False

def process_multiple_commands(command):

    commands = re.split(r"\s*(?:and|then|,)\s*", command.lower())

    last_action = ""

    for cmd in commands:

        cmd = cmd.strip()

        if not cmd:
            continue

        words = cmd.split()

        if words[0] in ["open", "close", "play"]:
            last_action = words[0]

        else:
            cmd = f"{last_action} {cmd}"

        print("Executing:", cmd) 
        processcommand(cmd)

def processcommand(c ):
    c = c.lower()

    if handle_apps_and_websites(c):
        return


    if handle_news(c):
        return

    if handle_information(c):
        return


    if handle_system(c):
        return
    
    else:
        output = ask_ai(c)
        speak(output)

if __name__ == "__main__":
    speak("Jarvis initializing...")

    r = sr.Recognizer()

    while True:

        if is_speaking:
            time.sleep(0.1)
            continue

    # microphone code here...
        print("Recognizing...")

        try:
            # Listen continuously
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=2)
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=10)

            text = r.recognize_google(audio).lower()
            print("Heard:", text)

            # Check for wake word
            if "jarvis" in text:

                # Remove wake word
                command = text.replace("jarvis", "", 1).strip()

                # -------------------------------
                # Case 1: User said
                # "Jarvis open Spotify"
                # -------------------------------
                if command:
                    process_multiple_commands(command)

                # -------------------------------
                # Case 2: User only said
                # "Jarvis"
                # -------------------------------
                else:
                    speak("Yes boss")

                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=0.5)
                        print("Jarvis Active!")
                        audio = r.listen(
                            source,
                            timeout=5,
                            phrase_time_limit=10
                        )

                    command = r.recognize_google(audio)
                    print(command)

                    process_multiple_commands(command)

        except Exception as e:
            print("Error:", e)
