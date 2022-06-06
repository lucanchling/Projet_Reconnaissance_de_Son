import sounddevice as sd 
from scipy.io.wavfile import write
import wavio as wv
import time, keyboard
from pydub import AudioSegment
import pyaudio 
import wave 
from random import randint

def record_micro(seconds):
    freq = 44100
    duration = seconds
    print("Press Space To start")
    if keyboard.read_key() == 'space' :
        print("Go")
        recording = sd.rec(int(duration * freq), samplerate = freq, channels = 1)
    sd.wait(seconds) 
    print("end")

    write("./music/music_to_compare.wav",freq,recording)
  
    
record_micro(15)

def random_mono_extract_from_file(duree : int, choix_music : str):
    
    sound = AudioSegment.from_wav('./music/music'+choix_music+'.wav')
    sound = sound.set_channels(1)

    duree = 10000  # une seconde est égale à 1000
    debut = randint(0,len(sound)-duree)
    fin = debut + duree 
    
    slice = sound[debut:fin]
    slice.export('./music/music_to_compare_mono.wav', format='wav')
    
   
