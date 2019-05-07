import os

list = os.listdir('.')
print
list
FichList = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f))]
print
len(FichList)

listFile = ('Fichier1.txt', 'Fichier2.tar.gz', 'Fichier3.gz.tu')
listFileSplit = []
listFinal = []
for x in FichList:
    listFileSplit.append(x.split("."))
for x in listFileSplit:
    listFinal.append(x[0])

print("FichList")
print
FichList
print("ListFileSplit")
print
listFileSplit
print("listFinale")
print
listFinal
