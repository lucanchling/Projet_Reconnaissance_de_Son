import scipy.io.wavfile as wavfile
import scipy.fftpack as fftpack
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import matplotlib.mlab as mlab
import os
import sys


def create_mono(file):
    """
    Create a mono file from the given file if it ain't already the case.
    :param file: path to the file
    :return: None
    """
    # Check if the file isn't a mono
    number = file[-5] # Check the number of the music
    if number.isdigit():    # It ain't a mono
        number = int(number)
        # If there's no mono file, create it
        if not os.path.isfile(file[:-4] + "_mono.wav"):
            sound = AudioSegment.from_file(file, format="wav")
            sound = sound.set_channels(1)
            sound.export(file[:-4] + "_mono.wav", format="wav")


# Function to locate peaks in the spectrogram of the music
from scipy.ndimage.morphology import (generate_binary_structure, iterate_structure, binary_erosion)
from scipy.ndimage.filters import maximum_filter

AMPLITUDE_PEAKS_MIN = 10    # minimum amplitude of peaks to be detected
NEIGHBORHOOD_SIZE = 20      # number of neighboring peaks to be considered

def get_2D_peaks(arr2D, plot=False, amp_min=AMPLITUDE_PEAKS_MIN, size_neighborhood=NEIGHBORHOOD_SIZE):
    # http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.morphology.iterate_structure.html#scipy.ndimage.morphology.iterate_structure
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, size_neighborhood)

    # find local maxima using our fliter shape
    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
    background = (arr2D == 0)
    eroded_background = binary_erosion(background, structure=neighborhood,
                                       border_value=1)

    # Boolean mask of arr2D with True at peaks
    detected_peaks = local_max ^ eroded_background

    # extract peaks
    amps = arr2D[detected_peaks]
    j, i = np.where(detected_peaks)

    # filter peaks
    amps = amps.flatten()
    peaks = zip(i, j, amps)
    peaks_filtered = [x for x in peaks if x[2] > amp_min]  # freq, time, amp

    # get indices for frequency and time
    frequency_idx = [x[1] for x in peaks_filtered]
    time_idx = [x[0] for x in peaks_filtered]

    # scatter of the peaks
    if plot:
      fig, ax = plt.subplots(figsize=(25, 10))
      ax.imshow(arr2D)
      ax.scatter(time_idx, frequency_idx)
      ax.set_xlabel('Time')
      ax.set_ylabel('Frequency')
      ax.set_title("Spectrogram")
      plt.gca().invert_yaxis()
      plt.show()

    return list(zip(frequency_idx, time_idx))


# Funtion to generate the spectrogram of the music

NFFT = 4096 # FFT size
noverlap = int(NFFT/2)

def spectrogram(data, fs, nfft=NFFT, noverlap=noverlap):
    """
    Generate the spectrogram of the given data.
    :param data: data to be analyzed
    :param fs: sampling frequency
    :param nfft: FFT size
    :param noverlap: overlap between two consecutive windows
    :return: spectrogram
    """
    # Compute the spectrogram
    arr2D = mlab.specgram(
        data,
        NFFT=NFFT,
        Fs=fs,
        window=mlab.window_hanning,
        noverlap=noverlap)[0]
    
    # apply log transform since specgram() returns linear array
    arr2D = 10 * np.log10(arr2D) # calculates the base 10 logarithm for all elements of arr2D
    arr2D[arr2D == -np.inf] = 0  # replace infs with zeros

    return arr2D

# Function to generate the hashes

from operator import itemgetter
import hashlib
from typing import List, Tuple

# Variables
FINGERPRINT_PARING_DEGREE = 15
FINGERPRINT_REDUCTION = 20  # Pour optimiser la taille du hash
# pour savoir si une fingerprint est proche d'une autre
min_hash = 0
max_hash = 200

def generate_hashes(peaks: List[Tuple[int, int]], fan_value: int = FINGERPRINT_PARING_DEGREE) -> List[Tuple[str, int]]:
    """
    Hash list structure:
       sha1_hash[0:FINGERPRINT_REDUCTION]    time_offset
        [(e05b341a9b77a51fd26, 32), ... ]
    :param peaks: list of peak frequencies and times.
    :param fan_value: degree to which a fingerprint can be paired with its neighbors.
    :return: a list of hashes with their corresponding offsets.
    """
    # frequencies are in the first position of the tuples
    idx_freq = 0
    # times are in the second position of the tuples
    idx_time = 1

    peaks.sort(key=itemgetter(1))

    hashes = []
    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):

                freq1 = peaks[i][idx_freq]
                freq2 = peaks[i + j][idx_freq]
                t1 = peaks[i][idx_time]
                t2 = peaks[i + j][idx_time]
                t_delta = t2 - t1

                if min_hash <= t_delta <= max_hash:
                    h = hashlib.sha1(f"{str(freq1)}|{str(freq2)}|{str(t_delta)}".encode('utf-8'))

                    hashes.append((h.hexdigest()[0:FINGERPRINT_REDUCTION], t1))

    return hashes

def write_hash_txt(hashes: List[Tuple[str, int]], file_name: str) -> None:
    """
    Write the hashes to a text file.
    :param hashes: the list of hashes.
    :param file_name: the name of the file to write to.
    :return: None
    """
    with open(file_name, 'w') as f:
        for h, t in hashes:
            f.write("{} {}\n".format(h, t))

def read_hash_txt(file_name: str) -> List[Tuple[str, int]]:
    """
    Read the hashes from a text file.
    :param file_name: the name of the file to read from.
    :return: the list of hashes.
    """
    hashes = []
    with open(file_name, 'r') as f:
        for line in f:
            h, t = line.strip().split(" ")
            hashes.append((h, int(t)))

    return hashes

########
# Main #
########
if __name__ == "__main__":
    # Variables
    PATH = './music/'

    # To check if the mono version of each music is already created (if not --> it generates it)
    for file in os.listdir(PATH):
        if file.endswith(".wav"):
            #print(file)
            create_mono(PATH + file)
    # We go through each music and we analyse each of them (only the mono version)
    nb = 0
    for file in os.listdir(PATH):
        if file.endswith("_mono.wav"):
            nb = nb + 1
            print(file)
            print("début du traitement...")
            print("lecture du fichier...")
            fs, data = wavfile.read(PATH + file)    # reading the mono version of the music
            print("calcul du spectrogram...")
            spectrogram_music = spectrogram(data, fs)   # generating the spectrogram of the music
            print("calcul des peaks...")
            peaks = get_2D_peaks(spectrogram_music)  # find the peaks of the music
            print("calcul des hashes...")
            hashes = generate_hashes(peaks)  # generate the hashes of the music
            print("écriture des hashes dans le txt...")
            print(len(hashes))
            write_hash_txt(hashes, "./dbmusic/datamusic"+ str(nb)+ ".txt")  # write the hashes of the music in a text file
            
            

