import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
import os
import wikipedia
from googletrans import Translator
import pyautogui
import time
from datetime import datetime

recognizer = sr.Recognizer()
engine = pyttsx3.init()
translator = Translator()
newsapi = "e1742a2f70a947819669f1ac41017d73"
weather_api_key = "065452ad549f2e520e61f8a5d8510148" # Replace this with your real API key


def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()


def get_weather(city="Delhi"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        res = requests.get(url)
        data = res.json()
        
        if res.status_code == 200 and "main" in data:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp}°C with {desc}.")
        else:
            speak("I couldn't fetch the weather. Please check the city name or API key.")
            print("API response:", data)  # Debugging line
    except Exception as e:
        speak("An error occurred while fetching weather.")
        print(f"Error in get_weather: {e}")


def take_note(note):
    with open("notes.txt", "a") as f:
        f.write(note + "\n")
    speak("Note saved.")


def read_notes():
    try:
        with open("notes.txt", "r") as f:
            notes = f.readlines()
            if notes:
                for i, note in enumerate(notes, 1):
                    speak(f"Note {i}: {note.strip()}")
            else:
                speak("You have no notes.")
    except:
        speak("No notes found.")


def set_alarm(alarm_time):
    speak(f"Alarm set for {alarm_time}")
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == alarm_time:
            speak("Time to wake up!")
            break
        time.sleep(30)


def remember_this(info):
    with open("memory.txt", "w") as f:
        f.write(info)
    speak("Got it. I'll remember that.")


def recall_memory():
    try:
        with open("memory.txt", "r") as f:
            memory = f.read()
            speak(f"You asked me to remember: {memory}")
    except:
        speak("I don't remember anything.")


def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("http://google.com")
    elif "open youtube" in c:
        webbrowser.open("http://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("http://linkedin.com")
    elif "open instagram" in c:
        webbrowser.open("http://instagram.com")
    elif "open facebook" in c:
        webbrowser.open("http://facebook.com")
    elif c.startswith("play"):
        song = c.split(" ", 1)[1]
        link = musiclibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in library.")

    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/everything?q=india&language=en&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            speak("Here are the top headlines from India.")
            for i, article in enumerate(articles[:5], start=1):
                title = article.get('title')
                if title:
                    print(f"{i}. {title}")
                    speak(f"Headline {i}: {title}")
        else:
            speak("Unable to fetch news.")

    elif "weather" in c:
        words = c.split()
        if "in" in words:
            city = words[words.index("in") + 1]
        else:
            city = "Delhi"
        get_weather(city)

    elif "take a note" in c:
        note = c.replace("take a note", "").strip()
        take_note(note)

    elif "show notes" in c:
        read_notes()

    elif "set alarm" in c:
        time_str = c.replace("set alarm for", "").strip()
        set_alarm(time_str)

    elif "remember that" in c:
        info = c.replace("remember that", "").strip()
        remember_this(info)

    elif "what do you remember" in c:
        recall_memory()

    elif "search" in c:
        query = c.replace("search", "").strip()
        result = wikipedia.summary(query, sentences=2)
        speak(result)

    elif "Translate" in c:
        text = c.replace("Translate", "").strip()
        translator = Translator.translate(text, dest="hi")
        speak(translator.text)
    
    elif "translate" in c:
        try:
            text = c.replace("translate", "").strip()
            translated = translator.translate(text, dest="hi")
            speak(translated.text)
        except Exception as e:
            print("Translation error:", e)
        speak("Sorry, I couldn't translate that.")

    elif "volume up" in c:
        pyautogui.press("volumeup")
    elif "volume down" in c:
        pyautogui.press("volumedown")
    elif "mute" in c:
        pyautogui.press("volumemute")
    elif "unmute" in c:
        pyautogui.press("volumeunmute")

    elif "open calculator" in c:
        os.startfile("calc.exe")
    elif "open notepad" in c:
        os.startfile("notepad.exe")

    else:
        speak("Sorry, I didn't understand that command.")


if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                word = recognizer.recognize_google(audio)
                if word.lower() == "jarvis":
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Jarvis active...")
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        processCommand(command)
        except Exception as e:
            print(f"Error: {e}")

