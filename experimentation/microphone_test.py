import sounddevice as sd
import numpy as np

talking = False

def print_sound(indata, outdata, frames, time, status):
	global talking
	volume_norm = np.linalg.norm(indata)*10
	if volume_norm >= 3:
		talking = True
		print("|"*int(volume_norm))
	else:
		talking = False

		
with sd.Stream(callback=print_sound):
	sd.sleep(100000)