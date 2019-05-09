import pygame
import os

FichList = [f for f in os.listdir('/home/pi/Desktop/sons_animaux/') if
            os.path.isfile(os.path.join('/home/pi/Desktop/sons_animaux/', f))]

listFileSplit = []
listFinal = []
for x in FichList:
    listFileSplit.append(x.split("."))
for x in listFileSplit:
    listFinal.append(x[0])

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

for i in range(0, len(FichList) - 1):
    pygame.mixer.music.load('/home/pi/Desktop/sons_animaux/' + FichList[i])
    pygame.mixer.music.play()
    reponse = raw_input("Ecrire la reponse : ")
    nom_animal = listFinal[i]

    if nom_animal in reponse:
        print
        "Bravo tu as trouve"
    else:
        print
        "Oh non c est dommage"
print
reponse
print
FichList
