import sounddevice as sd 
from scipy.io.wavfile import write
import time, keyboard
from pydub import AudioSegment
import os
from random import randint

def record_micro(seconds):
    freq = 48000
    duration = seconds
    print("Press Space To start")
    if keyboard.read_key() == 'space' :
        print("Go")
        recording = sd.rec(int(duration * freq), samplerate = freq, channels = 1 )
    sd.wait(seconds) 
    print("end")

    write("./music/music_to_compare.wav",freq,recording)
  
    
# record_micro(15)

def random_mono_extract_from_file(duree : int, choix_music : str):
    '''
    Extract a random mono music from a file.
    :param duree: the duration of the music to extract in second.
    :param choix_music: the name of the music to extract.
    :return: None
    '''
    nb = 1
    for i in os.listdir("./music/"):
        if i.endswith(".wav"):
            if nb == int(choix_music):
                sound = AudioSegment.from_wav("./music/"+i)
                sound = sound.set_channels(1)
                duree = duree*1000  # une seconde est égale à 1000
                debut = randint(0,len(sound)-duree)
                fin = debut + duree
                slice = sound[debut:fin]
                slice.export('./music/music_to_compare_mono.wav', format='wav')
                break
            nb = nb + 1

random_mono_extract_from_file(15,4)
    
   
