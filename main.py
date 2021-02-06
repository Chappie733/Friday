from speech import *
from activator import Activator
from lang_manager import *
from executor import *
import sounddevice as sd
import numpy as np

lang = Language()
lang.load("italian.lang")
print(str(lang))

sr = SpeechRecognizer()
speaker = Speaker()
activator = Activator(lang)
executor = Executor(lang)

sr.adjust()

speaker.language = lang.speech_id
sr.language = lang.rec_id
set_wiki_language(lang.speech_id)

response = ""
talking, running = False, True

def callback(indata, outdata, frames, time, status):
    global talking
    volume_norm = np.linalg.norm(indata)*10
    talking = volume_norm >= 3

with sd.Stream(callback=callback):
    
    while running:
        sd.sleep(1000)
        if talking:
            print("Talking")
            response = sr.listen().lower().split()
            print("Understood: " + ' '.join(response))
            idx = activator.process(response)
            if activator.active:
        	
                feedback, cmd_found = executor.process(response)
                speaker.say(feedback)


                if 'stop' in response and not cmd_found:
                    running = False

clean()
