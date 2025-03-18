# Projet Majeur - Reconnaissance de Musique

Ce projet a été réalisé dans le cadre d'un projet de fin de cycle de majeur

## Installation
Plusieurs modules python ont été utilisés afin de réaliser notre projet. Lesquels devant être installés sur votre machine.
```bash
pip install numpy scipy matplotlib pydub multiprocessing sounddevice
```
**Vérifier si d'autres modules doivent être installés sur votre machine au cours de l'uitlisation et les installer en conséquence**
## Utilisation
### 1. Créer un répertoire **./wav/** pour mettre les musiques qui vont composer votre database (uniquement des ***.wav***)
```bash
mkdir wav
```
### 2. Lancer le script **shazam.py** avec la commande suivante 
```bash
python shazam.py
```
### 3. Si la database n'a pas déjà été générée, taper **y** au premier lancement 
(si le folder **./wav/** n'a pas été modifié pas besoin de le faire à chaque lancement)
```python
-- ANALYSE MUSIC FROM DB --
Do you want to analyse the music from the DB ? (y/n) : y
```
### 4. Choisir la méthode d'enregistrement du fichier audio à analyser
```python
-- MUSIC FROM USER --
What do you want to do ?
1. Record a music from a file at a random timing
2. Record a music from your microphone
3. Import your own recording
```
#### Description des différents choix :
1. Permet de générer une séquence audio, à partir des différents morceaux présents dans la database, avec un timing de départ définit aléatoirement et un durée à définir (supérieur à 10 secondes)
2. Permet de lancer un enregistrement à partir du microphone de votre machine.
3. Vous permet d'importer un fichier audio de votre choix (impérativement un ***.wav***) 

### 5. Lancer la reconnaissance du son en tapant y à la dernière demande utilisateur
```python
-- COMPARE MUSIC WITH DB --
Do you want to compare the music with the DB ? (y/n) : y
```
