from matplotlib.pyplot import plot
from numpy import array
from generate_hashes import generate_fingerprints
from pydub import AudioSegment
import os
from typing import List
from time import time
import multiprocessing as mp

def nb_of_music_in_db() -> int:
    """
    Count the number of music in the database.
    :return: the number of music in the database.
    """
    nb = 0
    for file in os.listdir("./wav/"):
        if file.endswith(".wav"):
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

def retrieve_hashes_from_db(nb_of_music : int) -> List[str]:
    """
    Retrieve the hashes of all the music present in the database.
    :param file_name: the name of the music to compare.
    :return: the list of hashes.
    """
    
    Hashes = [] # List of all the hashes of the music in the database
    for i in range(1, nb_of_music+1):
        # We read the hashes of the music
        hashes = read_hash_txt("./dbmusic/datamusic"+ str(i)+ ".txt")
        Hashes.append(hashes)

    return Hashes

def create_mono(full_path_of_file: str) -> None:
    """
    Create the mono version of the music.
    :param full_path_of_file: the name of the music to convert.
    :return: None
    """
    ########################
    # For Music To Compare #
    ########################
    if not os.path.exists(full_path_of_file) and os.path.exists(full_path_of_file[:-4] + "_mono.wav"):
        return
    else:
        sound = AudioSegment.from_file(full_path_of_file, format="wav")
        sound = sound.set_channels(1)
        sound.export(full_path_of_file[:-4] + "_mono.wav", format="wav")


def compare_hashes(Hashes: List[str],hashes_to_compare : List[str],indice : int, array) -> int:
    """
    Compare the hashes of the music with the hashes of the music in the database.
    :param Hashes: the list of all hashes
    :param hashes_to_compare: the list of hashes of the music in the database.
    :param indice: the index of the music in the database.
    :return: the number of hashes that are the same.
    """
    nb_of_hashes_found = 0
    for hash in Hashes[indice]:
        if hash in hashes_to_compare:
            nb_of_hashes_found = nb_of_hashes_found + 1
    
    # print("Nombre de matchs avec "+ get_music_name(indice) +  " :", nb_of_hashes_found)
    # We add the number of matches to the array which is shared between the processes
    array[indice] = nb_of_hashes_found
    #return nb_of_hashes_found


def get_music_name(indice: int) -> str:
    """
    Get the name of the music from the database.
    :param indice: the index of the music in the database.
    :return: the name of the music.
    """
    with open("./dbmusic/musicname.txt", 'r') as f:
        for i, line in enumerate(f):
            if i == indice:
                return line[:-1]


def find_music(Matches,threshold = 500) -> List[str]:
    """
    Find the music with the most matches.
    :param arr_matches: the array of the number of matches.
    :param threshold: the threshold used to find if the music to analyse suit with enough matches or not.
    :return: the name of the music with the most matches.
    """
    max_value = max(Matches)

    if max_value >= threshold:
        music_name = get_music_name(Matches.index(max_value))
        print("La musique recherchée est :",music_name)
    else :
        print("Aucune musique correspondante dans la database")

#def recognize_music():

if __name__ == "__main__":
    # Variables
    PATH = './music/'
        
    # We count the number of music in the database
    nb_of_music = nb_of_music_in_db()

    # PART ONE --> AQUISITION OF THE HASHES
    Hashes = retrieve_hashes_from_db(nb_of_music)
    
    # PART TWO --> COMPARISON OF THE HASHES
    create_mono(PATH + "music_to_compare.wav")
    
    # Generation of hash of the music we want to compare
    hashes_to_compare = generate_fingerprints("./music/music_to_compare_mono.wav",False)
    nb_of_hashes_to_compare = len(hashes_to_compare)
    print("Nombre de Hash à analyser : ",nb_of_hashes_to_compare)

    tic = time()
    process = []
    array_matches = mp.Array('i', range(nb_of_music))  # Array compatible with multiprocessing for counting the number of matchs
    for i in range(0, nb_of_music):
        process.append(mp.Process(target= compare_hashes,args=(Hashes,hashes_to_compare,i,array_matches)))
        process[i].start()       

    for i in range(0, nb_of_music):
        process[i].join()
    
    print("Temps d'execution pour l'analyse : ", round(time() - tic,2), "s")

    # PART THREE --> DISPLAY OF THE RESULTS
    #print(array_matches[:])
    Matches = array_matches[:]
    print(Matches)
    find_music(Matches,500)