import speech_recognition as sr
import webbrowser
import musiclibrary
import requests
from google import genai
import datetime
from gtts import gTTS
from dotenv import load_dotenv
import tempfile
import threading
import pygame
import time
import sys
import os

load_dotenv()

newsapi =  os.getenv("NEWS_API_KEY")


def speak(text):
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
        if os.path.exists(filename):
            os.remove(filename)

def speak_async(text):
    threading.Thread(
        target=speak,
        args=(text,),
        daemon=True
    ).start()

def aiprocess(command):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"answer is maximum 4 lines : {command}"
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

def processcommaand(c ):

    if "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open hub"in c.lower():
        webbrowser.open("https://github.com/PooravMSharma")
    elif "open hotstar" in c.lower():
        webbrowser.open("https://www.hotstar.com/in/onboarding/profile?ref=%2Fin%2Fhome")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com/")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/everything?q=india&sortBy=publishedAt&apiKey={newsapi}")

        if r.status_code == 200:
            data = r.json()

            articles = data.get('articles' , [])

            for i, article in enumerate(articles[:5], start=1):
                title = article["title"]
                print(f"{i}. {title}")
                speak_async(title)

    elif "time" in c.lower():
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak_async(f"The time is {time}")

    elif "date" in c.lower():
        date = datetime.datetime.now().strftime("%d %B %Y")
        speak_async(date)

    elif "open spotify" in c.lower():
        os.system("spotify")

    elif "open calculator" in c.lower():
        os.system("calc")

    elif "open vscode" in c.lower():
        os.system("code")

    elif "open netflix" in c.lower():
        webbrowser.open("https://www.netflix.com/in/")

    elif "open claude" in c.lower():
        webbrowser.open("https://claude.ai/new")

    elif "weather in" in c.lower():

        city = c.lower().split("weather in")[-1].strip()

        weather = get_weather(city)

        print(weather)
        speak_async(weather)

    elif "stop talking" in command:
        pygame.mixer.music.stop()

    elif "shutdown" in c.lower():
        speak("Goodbye boss")
        exit()

    elif "restart" in c.lower():
        speak("Restarting")

        os.execl(sys.executable, sys.executable, *sys.argv)
    
    else:
        output = aiprocess(c)
        speak_async(output)

if __name__ == "__main__":
    speak("Jarvis initializing.......")
    while True:

        r = sr.Recognizer()
        
        print("recognizing")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Listening...!")
                audio = r.listen(source , timeout=5 , phrase_time_limit=10)
            word = r.recognize_google(audio)  # type: ignore[attr-defined]
            if ("jarvis" in word.lower()):
                speak_async("yes boss")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=1)
                    print("jarvis active!")
                    audio = r.listen(source , timeout=5 , phrase_time_limit=10)
                    command = r.recognize_google(audio) # type: ignore[attr-defined]

                    processcommaand(command)
                    print(command)

        except Exception as e:
            print("Error; {0}".format(e))

