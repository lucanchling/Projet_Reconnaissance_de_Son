from imghdr import tests
import time
import compare_with_db as cwdb
import generate_hashes as gh
from record_song_to_analyze import record_micro, random_mono_extract_from_file
from random import randint
import os
from pydub import AudioSegment

def main():
    # Part ONE : Analyse Music from DB
    print("-- ANALYSE MUSIC FROM DB --")
    if str(input("Do you want to analyse the music from the DB ? (y/n) : ")) == "y":
        gh.main()

    # print()

    # Part TWO : Analyse Music from User
    print("-- MUSIC FROM USER --")
    print("What do you want to do ?")
    print("1. Record a music from a file at a random timing")
    print("2. Record a music from your microphone")
    print("3. Import your own recording")
    answer = int(input("Your choice : "))


    if answer == 1:
        duree = int(input("How long do you want to record (in seconds) ? "))
        choice = str(input("Which music do you want to record ? (1,2,3...) : "))
        random_mono_extract_from_file(duree,choice)
    elif answer == 2:
        duree = str(input("How long do you want to record (in seconds) ? "))
        record_micro(duree)
    elif answer == 3:
        print("You must put your file in the folder './music/'")
        print("The file name should be 'music_to_compare.wav'")
    

    print()

    # Part THREE : Compare the music
    print("-- COMPARE MUSIC WITH DB --")
    print("Do you want to compare the music with the DB ? (y/n)")
    if str(input()) == "y":
        cwdb.main()

def test():
    '''function to run some test to setup the threshold'''
    #main()
    lenhashes,maxmatches,secondmaxmatches = [],[],[]
    for file in os.listdir("./micro_not_in/"):
        print(file)
        sound = AudioSegment.from_wav("./micro_not_in/"+file)
        sound.export('./music/music_to_compare.wav', format='wav')
        time.sleep(1)
        lh, matches = cwdb.main()
        sortedmatches = sorted(matches)
        lenhashes.append(lh)
        maxmatches.append(max(matches))
        secondmaxmatches.append(sortedmatches[-2])
    
    print("Taille échantillons : ",lenhashes)
    print("Valeurs des maxmatches : ",maxmatches)
    print("Valeur des deuxième plus grandes valeurs de matches",secondmaxmatches)
    print("Moyenne des maxs : ", sum(maxmatches)/len(maxmatches))
    sortedmax = sorted(maxmatches)
    print("Valeur médianne : ", sortedmax[int(len(sortedmax)/2)])
    print("Premier Quartile : ", sortedmax[int(len(sortedmax)/4)])
    rapport = [maxmatches[i]/lenhashes[i] for i in range(len(lenhashes))]
    print("Moyenne des rapports max/len:",sum(rapport)/len(lenhashes))
    diffmaxsecond = [maxmatches[i]-secondmaxmatches[i] for i in range(len(maxmatches))]
    print("diff : ",diffmaxsecond)
    print("Diff moyenne :",sum(diffmaxsecond)/len(diffmaxsecond))

if __name__ == "__main__":
    #main()
    test()