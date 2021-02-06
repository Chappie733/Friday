import gtts
from playsound import playsound
import speech_recognition as sr
import os

class Speaker:

    def __init__(self, language=None):
        self.language = language

    def say(self, text):
        if len(text) == 0:
            return
        print(text)
        tts = gtts.gTTS(text, lang=self.language)
        filename = "speech\\speech_" + str(len(os.listdir("speech"))) + ".mp3"
        tts.save(filename)
        playsound(filename)

def clean():
    files = os.listdir("speech")
    for file in files:
        os.remove(os.path.dirname(os.path.abspath(__file__)) + "\\speech\\"+file)

class SpeechRecognizer():
    DEFAULT_LANGUAGE = 'en-US'

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.adjusted = False
        self.language = self.DEFAULT_LANGUAGE

    def adjust(self):
        with self.mic as source:
            if not self.adjusted:
                self.recognizer.adjust_for_ambient_noise(source)
                self.adjusted = True
                print("Audio recognition adjusted for ambient noise...")

    def listen(self):
        response = ""
        with self.mic as source:
            audio = self.recognizer.listen(source)
            try:
                response = self.recognizer.recognize_google(audio, language=self.language)
            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return response
