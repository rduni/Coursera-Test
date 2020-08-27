import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
import requests, json
import vlc
api_key = "805fbece070b62d546f8a053f6846c0b"
base_url = "http://api.openweathermap.org/data/2.5/weather?" #generate weather api

engine = pyttsx3.init()
#voices = engine.getProperty('voices')
# print(voices[1].id)
#engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Jarvis Sir. Please tell me the password")
    query = takeCommand().lower()
    if query == '1':
        speak("Hello Rohit sir, what can i do for you")
    else:
        speak("Sorry sir you are not authorised ")
        exit()       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('rohitdatta1998@gmail.com', 'DattaKutta')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   


        elif 'play music' in query:
            music_dir = '/home/datta/Downloads/songs'
            songs = os.listdir(music_dir)
            print(songs)
            p = vlc.MediaPlayer("/home/datta/Downloads/songs/06. I Don't Care.mp3")
            p.play()
            #os.system(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        
        elif 'email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "rohitdatta1998@gmail.com"   
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend harry bhai. I am not able to send this email")    
        
        elif 'weather' in query:
            os.system('espeak "which city sir"')
            audio_city = takeCommand()
            
            complete_url = base_url + "appid=" + api_key + "&q=" + audio_city
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":

                y = x["main"]
                current_temperature = str(y["temp"])
                current_pressure = str(y["pressure"])
                current_humidiy =str(y["humidity"])
                z = x["weather"]

                weather_description = str(z[0]["description"])
                os.system('espeak '+current_temperature+"degree" + "farenheit"'')
                os.system('espeak '+ current_pressure + "hecto" + "pascal"'')
                os.system('espeak '+ current_humidiy + "percentage" '')
                os.system('espeak '+weather_description +'')
        elif 'terminate' in query:
            speak("than you for using jarvis sir .See you soon")
            exit()
