from generate_hashes import generate_fingerprints
from pydub import AudioSegment
import os
from typing import List, Tuple
import numpy as np
from time import time


def nb_of_music_in_db() -> int:
    """
    Count the number of music in the database.
    :return: the number of music in the database.
    """
    nb = 0
    for file in os.listdir("./dbmusic/"):
        if file.endswith(".txt"):
            nb = nb + 1

    return nb

def read_hash_txt(file_name: str) -> List[str]:
    """
    Read the hashes of the music from a text file with erasing the \n at the end of each line.
    :param file_name: the name of the text file.
    :return: the list of hashes.
    """
    with open(file_name, 'r') as f:
        hashes = []
        for line in f:
            hashes.append(line[:-1])
    return hashes

def create_mono(file: str) -> None:
    """
    Create the mono version of the music.
    :param file_name: the name of the music to convert.
    :return: None
    """
    ########################
    # For Music To Compare #
    ########################
    if not os.path.isfile(file[:-4] + "_mono.wav"):
        sound = AudioSegment.from_file(file, format="wav")
        sound = sound.set_channels(1)
        sound.export(file[:-4] + "_mono.wav", format="wav")

if __name__ == "__main__":
    # Variables
    PATH = './music/'

    # PART ONE --> AQUISITION OF THE HASHES
    # We count the number of music in the database
    nb_music_in_db = nb_of_music_in_db()
    Hashes = [] # List of all the hashes of the music in the database
    for i in range(1, nb_music_in_db+1):
        # We read the hashes of the music
        hashes = read_hash_txt("./dbmusic/datamusic"+ str(i)+ ".txt")
        Hashes.append(hashes)
    

    # PART TWO --> COMPARISON OF THE HASHES
    # Generation of hash of the music we want to compare
    create_mono(PATH + "music_to_compare.wav")
    hashes_to_compare = generate_fingerprints("./music/music_to_compare_mono.wav")
    nb_of_hashes_to_compare = len(hashes_to_compare)
    print(nb_of_hashes_to_compare)

    tic = time()
    for i in range(0, nb_music_in_db):
        print("Comparaison avec la musique " + str(i+1))
        # We compare the hashes of the music we want to compare with the hashes of the music in the database
        nb_of_hashes_found = 0
        for hash in Hashes[i]:
            if hash in hashes_to_compare:
                nb_of_hashes_found = nb_of_hashes_found + 1

        # We print the result
        print("Nombre de matchs : ", nb_of_hashes_found)
    print("Temps de calcul : ", round(time() - tic, 3), "s")
