import sounddevice as sd 
from scipy.io.wavfile import write
import wavio as wv
import time, keyboard
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

def record_from_laptop_sound(filename: str):
    
    chunk = 1024  
  
    sample_format = pyaudio.paInt16   
    chanels = 1
    
    freq = 44100  
    seconds = 10
    
    
    pa = pyaudio.PyAudio()   
    
    stream = pa.open(format=sample_format, channels=chanels,  
                    rate=freq, input=True,  
                    frames_per_buffer=chunk) 
    
    print('Recording...') 
    
    frames = []   
    
    for i in range(0, int(freq / chunk * seconds)): 
        data = stream.read(chunk) 
        frames.append(data) 
    
    stream.stop_stream() 
    stream.close() 
    
    pa.terminate() 
    
    print('Done !!! ') 
    
    sf = wave.open(filename, 'wb') 
    sf.setnchannels(chanels) 
    sf.setsampwidth(pa.get_sample_size(sample_format)) 
    sf.setframerate(freq)
    sf.writeframes(b''.join(frames)) 
    sf.close() 
    
record_from_laptop_sound('./music/music1.wav')