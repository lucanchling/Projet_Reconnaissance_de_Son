import numpy as np


def compute_similarity(ref_rec,input_rec,weightage=[0.33,0.33,0.33]):
    '''Permet de calculer les similarités entre deux signaux'''
    ## Time domain similarity
    ref_time = np.correlate(ref_rec,ref_rec)    
    inp_time = np.correlate(ref_rec,input_rec)
    diff_time = abs(ref_time-inp_time)

    ## Freq domain similarity
    ref_freq = np.correlate(np.fft.fft(ref_rec),np.fft.fft(ref_rec)) 
    inp_freq = np.correlate(np.fft.fft(ref_rec),np.fft.fft(input_rec))
    diff_freq = abs(ref_freq-inp_freq)

    ## Power similarity
    ref_power = np.sum(ref_rec**2)
    inp_power = np.sum(input_rec**2)
    diff_power = abs(ref_power-inp_power)

    return float(weightage[0]*diff_time+weightage[1]*diff_freq+weightage[2]*diff_power)

def diff_zero(signal):
    '''Permet de supprimer les zéros en début et fin de signal'''
    for i in range(len(signal)):
        if signal[i] != 0:
            ind1 = i
            break
    for i in range(len(signal)-1,0,-1):
        if signal[i] != 0:
            ind2 = i
            break
    return signal[ind1:ind2+1]