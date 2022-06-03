import sounddevice as sd 
from scipy.io.wavfile import write
import wavio as wv
import time, keyboard
from pydub import AudioSegment
import pyaudio 
import wave 

def record_micro(seconds):
    freq = 44100
    duration = seconds
    print("Press Space To start")
    if keyboard.read_key() == 'space' :
        print("Go")
        recording = sd.rec(int(duration * freq), samplerate = freq, channels = 1)
    sd.wait(seconds) 
    print("end")

    write("record.wav",freq,recording)


    #wv.write("recording1.wav", recording, freq, sampwidth=2)
    
    
#record_micro(10)

def record_from_laptop_sound(choix :int ):
    
    audio = AudioSegment.from_wav('./music/music'+str(choix)+'.wav')
    #return audio

record_from_laptop_sound(3)
