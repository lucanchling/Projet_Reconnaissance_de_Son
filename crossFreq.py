import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.io import wavfile
import scipy.signal as signal

np.seterr(all='raise')

def fstereo2mono(dataSte):
    #methode de calcul non opti; à changer
    dataMono = np.zeros(len(dataSte))
    for i in range(len(dataSte)):
        dataMono[i] = dataSte[i][0]/2 + dataSte[i][1]/2
    return dataMono

def fNormalize(data):
    max = np.amax(data)
    #print("max : ", max)
    dataN = np.zeros(len(data))
    for i in range(len(data)):
        dataN[i] = data[i]/max
    return dataN

try:
    # Fichier 1
    Ts1, data1 = wavfile.read("bassbones.wav")
    temps1 = np.linspace(0,len(data1)*1/Ts1,len(data1))
    # Fichier 2
    Ts2, data2 = wavfile.read("test.wav")
    temps2 = np.linspace(0,len(data2)*1/Ts2,len(data2))
    print("[Fin d'importation]")
	
	
    # Gestion Stéréo 
    if type(data1[0]) == type(data1):
        #si stéréo premier element = array; si mono premier element = int
        data1 = fstereo2mono(data1)
    if type(data2[0]) == type(data2):
        data2 = fstereo2mono(data2)
	
	print("[Fin Conversion Stereo Mono]")
    
	data1 = fNormalize(data1)
    data2 = fNormalize(data2)

    N = 1024
    DATA1 = np.fft.fft(data1, N)
    freq1 = np.fft.fftfreq(N)
    DATA2 = np.fft.fft(data2, N)
    freq2 = np.fft.fftfreq(N)

    acorrel = signal.correlate(data1, data1, mode='full', method='auto')
    xcorrel = signal.correlate(data1, data2, mode='full', method='auto')
    
	
    #plt.plot(xcorrel,linewidth=0.43)
	
    plt.plot(freq1, abs(DATA1), linewidth=0.6)
    #plt.plot(freq2, abs(DATA2), linewidth=0.43)
    #plt.plot(xcorrel, linewidth=0.43)
    plt.show()
    
except NameError:
    print("--------------ERROR OCCURED--------------")
    print(NameError)



"""
#bpm 
# max auto et inter et moyenne en abs 
et en freq 
#xcorr en freq 
tfd sur memenb de piont

"""