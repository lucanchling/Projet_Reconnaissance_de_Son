import compare_with_db as cwdb
import generate_hashes as gh
from record_song_to_analyze import record_micro, random_mono_extract_from_file
from random import randint

if __name__ == "__main__":
    
    # Part ONE : Analyse Music from DB
    print("-- ANALYSE MUSIC FROM DB --")
    if str(input("Do you want to analyse the music from the DB ? (y/n) : ")) == "y":
        gh.main()

    print()

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
    
