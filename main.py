import pyttsx3
import datetime
import webbrowser
import time
import speech_recognition as sr
import pyautogui
import os
import sys
import psutil

import json 
import pickle 
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences 
import numpy as np 
# from elevenlabs import play,Voice
# from api_key import key_data

# voice = Voice(name="Grace", api_key=key_data)
# # set_api_key(key_data)

# def engine_talk(query):
#     audio = voice.generate(text=query)  
#     # audio = generate(
#     #     text=query, 
#     #     voice='Grace',
#     #     model="eleven_monolingual_v1"
#     # )
#     play(audio)
with open("intents.json") as file:
    data=json.load(file)
model=load_model("chat_model.h5")
with open("tokenizer.pkl","rb") as f:
    tokenizer=pickle.load(f)
with open("label_encoder.pkl","rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)




def initialize_engine():
    engine=pyttsx3.init("sapi5")
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    rate=engine.getProperty("rate")
    engine.setProperty('rate',rate-50)
    volume=engine.getProperty('volume')
    engine.setProperty('volume',volume+0.25)
    return engine

def speak(text):
    engine=initialize_engine()
    engine.say(text)
    engine.runAndWait()


def command():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.5)
        print("Listening....",end="",flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate=48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustement_damping=2
        r.energy_threshold=4000
        r.phrase_time_limit=10
        # print(sr.Microphone.list_microphone_names())
        audio=r.listen(source)
        try:
            print("\r",end="",flush=True)
            print("recognizing....",end="",flush=True)
            query=r.recognize_google(audio,language='en-in')
            print(f"user said: {query}\n")
        except:
            print("say that again please")
            return "None"
        return query
def cal_day():
    day=datetime.datetime.today().weekday()+1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week=day_dict[day]
        print(day_of_week)
    return day_of_week
def wishMe():
    hour=int(datetime.datetime.now().hour)
    t=time.strftime("%I:%M:%p")
    day=cal_day()
    if(hour>=0) and (hour<=12)  and ('AM' in t):
        speak(f"Good morning sneha,it's {day} and the time is {t}") 
    elif(hour>=12) and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon sneha,it's {day} and the time is {t}")
    else:
        speak(f"Good  evening sneha,it's {day} and the time is {t}")

def social_media(command):
    if 'facebook' in command:
        speak("opeing your facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("opening whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'discord' in command:
        speak("opening discord server")
        webbrowser.open("https://discord.com/")
    elif 'instagram' in command:
        speak("opening instagram")
        webbrowser.open("https://www.instagram.com/")
    else:
        speak("No result found")

def schedule():
    day=cal_day().lower()
    speak("Boss today's schedule is ")
    week={
        "monday":"Boss, from 9:00 am to 9:50 am you have compiler design class, from 10:00 am to 10:50 am you have computer networks class",
        "tuesday": "Boss, from 9:00 am to 9:50 am you have operating systems class, from 10:00 am to 10:50 am you have database management systems class",
    "wednesday": "Boss, from 9:00 am to 9:50 am you have data structures class, from 10:00 am to 10:50 am you have algorithms class",
    "thursday": "Boss, from 9:00 am to 9:50 am you have theory of computation class, from 10:00 am to 10:50 am you have software engineering class",
    "friday": "Boss, from 9:00 am to 9:50 am you have artificial intelligence class, from 10:00 am to 10:50 am you have machine learning class",
    "saturday": "Boss, from 9:00 am to 9:50 am you have cloud computing class, from 10:00 am to 10:50 am you have cyber security class",
    "sunday": "Boss, it's a rest day. No classes scheduled!"
    }
    if day in week.keys():
        speak(week[day])

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile("C:\\Windows\\System32\\calc.exe")
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile("C:\\Windows\\System32\\notepad.exe")
    elif "paint" in command:
        speak("opening painting")
        os.startfile("C:\\Users\\vdine\\AppData\\Local\\Microsoft\\WindowsApps\\mspaint.exe")
def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system("taskkill /f /im calc.exe")
        
    elif "notepad" in command:
        speak("closing notepad")
        os.system("taskkill /f /im notepad.exe")
    elif "paint" in command:
        speak("closing painting")
        os.system("taskkill /f /im mspaint.exe")
def browsing(query):
    if 'google' in query:
        speak("Boss,what should i search on google...")
        s=command()
        unnecessary_phrases = [
    "search about","look up","find information on","tell me about",
    "what is","how to","who is","can you tell me","I want to know about",
    "please look for","show me","give me information on","find",
    "search for","google","can you find","look for"
]
        s=s.lower()
        for phrase in unnecessary_phrases:
            s = s.replace(phrase, "").strip()

        chrome_path="C:\Program Files\Google\Chrome\Application\chrome.exe"
        webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open(f"https://www.google.com/search?q={s}")
def condition():
    usage=str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery=psutil.sensors_battery()
    percentage=battery.percent
    power_plug=battery.power_plugged
    speak(f"Boss our system have {percentage} percentage battery")
    
    if power_plug:
        speak("the charger is plugged in")
    else:
        speak("charger is not plugged in")
    

    if percentage>=80:
         speak("we could have enough charing to continue working")
    elif 40 <= percentage < 75:
        if not power_plug:
            speak("we should connect our system to charger")
    else:
        if not power_plug:
            speak("Immediately connect to charger")

if __name__=="__main__":
    wishMe()
    # engine_talk("hello how can i help you")
    while True:
        query=command().lower()
        # query=input("Enter your command:")
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)
        elif ("university time table" in query) or ('schedule' in query):
            schedule()
        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup") 
            speak("volume increased")
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown") 
            speak("volume decreased")
        elif ("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volume muted") 
            speak("muted")
        elif ("open calculator" in query) or ("open notepad" in query) or ('open paint' in query):
            openApp(query)
        elif ("close calculator" in query) or ("close notepad" in query) or ("close paint"in query):
            closeApp(query)
        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
            padded_sequences=pad_sequences(tokenizer.texts_to_sequences([query]),maxlen=20,truncating='post')
            result=model.predict(padded_sequences)
            tag=label_encoder.inverse_transform([np.argmax(result)])
            for i in data['intents']:
               if i['tag']==tag:
                  speak(np.random.choice(i['responses']))
        elif ("open google" in query):
            browsing(query) 
        elif   ("system condition" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()
        elif  "exit" in query:
            sys.exit()

        
       
# speak("Hello i am chatbot")
