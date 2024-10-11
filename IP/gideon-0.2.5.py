'''
    Description: 
    Author: Julian Principe, AVM, Blackbox
    Version: 0.2.5
'''
import AVMSpeechMath as sm
import AVMYT as yt
import speech_recognition as sr
import pyttsx3
import pywhatkit
import json
from datetime import datetime, date, timedelta
import wikipedia
import pyjokes
from time import time

start_time = time()
engine = pyttsx3.init()

# name of the virtual assistant
name = 'gideon'
attemts = 0

# keys
with open('src/keys.json') as json_file:
    keys = json.load(json_file)

# colors
green_color = "\033[1;32;40m"
red_color = "\033[1;31;40m"
normal_color = "\033[0;37;40m"

# get voices and set the first of them
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# editing default configuration
engine.setProperty('rate', 178)
engine.setProperty('volume', 0.9)

day_es = [line.rstrip('\n') for line in open('src/day/day_es.txt')]
day_en = [line.rstrip('\n') for line in open('src/day/day_en.txt')]

def iterateDays(now):
    for i in range(len(day_en)):
        if day_en[i] in now:
            now = now.replace(day_en[i], day_es[i])
    return now

def getDay():
    now = date.today().strftime("%A, %d de %B del %Y").lower()
    return iterateDays(now)

def getDaysAgo(rec):
    value =""
    if 'ayer' in rec:
        days = 1
        value = 'ayer'
    elif 'anteayer' in rec:
        days = 2
        value = 'antier'
    else:
        rec = rec.replace(",","")
        rec = rec.split()
        days = 0

        for i in range(len(rec)):
            try:
                days = float(rec[i])
                break
            except:
                pass
    
    if days != 0:
        try:
            now = date.today() - timedelta(days=days)
            now = now.strftime("%A, %d de %B del %Y").lower()

            if value != "":
                return f"{value} fue {iterateDays(now)}"
            else:
                return f"Hace {days} días fue {iterateDays(now)}"
        except:
            return "Aún no existíamos"
    else:
        return "No entendí"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    status = False

    with sr.Microphone() as source:
        print(f"{green_color}({attemts}) Escuchando...{normal_color}")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        rec = ""

        try:
            rec = r.recognize_google(audio, language='es-ES').lower()
            
            if name in rec:
                rec = rec.replace(f"{name} ", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                status = True
            else:
                print(f"Vuelve a intentarlo, no reconozco: {rec}")
        except:
            pass
    return {'text':rec, 'status':status}

while True:
    rec_json = get_audio()

    rec = rec_json['text']
    status = rec_json['status']

    if status:
        if 'estas ahi' in rec:
            speak('Por supuesto')

        elif 'reproduce' in rec:
                music = rec.replace('reproduce', '')
                speak(f'Reproduciendo {music}')
                #yt.play(music)
                pywhatkit.playonyt(music)
        
        elif 'cuantos suscriptores tiene' in rec:
            name_subs = rec.replace('cuantos suscriptores tiene', '')
            
            speak("Procesando...")
            while True:
                try:
                    channel = yt.getChannelInfo(name_subs)
                    speak(channel["name"] + " tiene " + channel["subs"])
                    break
                except:
                    speak("Volviendo a intentar...")
                    continue

        elif 'que' in rec:
            if 'hora' in rec:
                hora = datetime.now().strftime('%I:%M %p')
                speak(f"Son las {hora}")

            elif 'dia' in rec:
                if 'fue' in rec:
                    speak(f"{getDaysAgo(rec)}")
                else:
                    speak(f"Hoy es {getDay()}")
                    
        elif 'qué' in rec:
            if 'hora' in rec:
                hora = datetime.now().strftime('%I:%M %p')
                speak(f"Son las {hora}")
                
            elif 'día' in rec:
                if 'fué' in rec:
                    speak(f"{getDaysAgo(rec)}")
                else:
                    speak(f"Hoy es {getDay()}")

        elif 'busca' in rec:
            order = rec.replace('busca', '')
            wikipedia.set_lang("es")
            info = wikipedia.summary(order, 1)
            speak(info)

        elif 'chiste' in rec:
            chiste = pyjokes.get_joke("es")
            speak(chiste)

        elif 'cuanto es' in rec:
            speak(sm.getResult(rec))
            
        elif 'genio' in rec:
            speak("Julian Principe, por supuesto. Futuro experto programador de Inteligencia Artificial, experto en pyton, Deep Learning. AH, y mi programador.")

        elif 'todo bien' in rec:
            speak("Por Supuesto.¿Quieres que te ayude con algo?")

        elif 'si' in rec:
            speak("Adelante. Dime en que te puedo ayudar...")
            
        elif 'buenos dias' in rec:
            speak("Buenos Días. Espero que tengas un muy lindo día")
            
        elif 'buenas noches' in rec:
            speak("Buenas noches")

        elif 'no' in rec:
            speak("¿Seguro?Bueno, cuando necesites algo, di gideon y lo que quieras que haga")

        elif 'gracias' in rec:
            speak("De nada. Estoy aqui para ayudarte.¿Necesitas algo?")

        elif 'mierda' in rec:
            speak("Bueno, no es necesario insultar.¿necesitas otra cosa?")
            
        elif 'clarita' in rec:
            speak("Clarita es una chica que le interesa actuar. Sabe matematica, y le gusta la geometría")
            
        elif 'pochoclo' in rec:
            speak("Jean Luka Ronco, también conocido como Pochoclo es un chico al que le gusta el básket, Escucha música de verdad, y tiene un hermano que es Senior, Desarrollador Web. Es también un Gil muy importante")

        elif "bueno" in rec:
            speak("Tengo más.¿Quieres otro?")

        elif 'espectacular' in rec:
            speak("Gracias. ¿Algo mas?")
            
        elif 'leon' in rec:
            speak("León es una persona que le gusta excesivamente el helado de limon granizado, le gusta jugar juegos de destruir cosas, y tiene dos huracanes que se hacen llamar  Hermanitos, uno tiene calidad y le interesa la programacion, y el otro es una mezcla de falopa futbolistica, y fortnait. ")
            
        elif 'felix' in rec:
            speak("felix es un drogadicto quimico, y no sabe javascript")
            
        elif 'gael' in rec:
            speak("gael es un judio comunista interesado por la fisica y la matematica, como el desarrollador de este asistente")
        
        elif 'no' in rec:
            speak("¿Seguro?Bueno, cuando necesites algo, di gideon y lo que quieras que haga")

        elif 'descansa' in rec:
            speak("Saliendo...")
            break

        else:
            print(f"Vuelve a intentarlo, no reconozco: {rec}")
        
        attemts = 0
    else:
        attemts += 1

print(f"{red_color} PROGRAMA FINALIZADO CON UNA DURACIÓN DE: { int(time() - start_time) } SEGUNDOS {normal_color}")
        