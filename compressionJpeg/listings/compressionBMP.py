from PIL import Image
import numpy as np
from math import *

# RECUPERATION DE L'IMAGE

# ouvre l'image
image = Image.open('static/pictures/bitmap_picture.bmp')

# Convertir l'image en niveaux de gris
image = image.convert('L')

# matrice
pixels = image.load()

# Dimensions de l'image
largeur, hauteur = image.size

# Créer une matrice vide pour stocker les pixels
matrice = []

# Parcourir tous les pixels et les ajouter à la matrice
for y in range(hauteur):
    ligne = []
    for x in range(largeur):
        pixel = pixels[x, y]
        ligne.append(pixel)
    matrice.append(ligne)

# Enregistrez la matrice dans un fichier texte
with open('matrice_pixels.txt', 'w') as fichier:
    for ligne in matrice:
        ligne_texte = ' '.join(map(str, ligne))
        fichier.write(ligne_texte + '\n')

# DECOUPAGE EN BLOCS DE 8X8 PIXELS

def decoupage8x8():
    largeur, hauteur = image.size

    # Initialiser une liste pour stocker les blocs
    matrice_blocs_8x8 = []

    # Parcourir l'image en blocs de 8x8 pixels
    for hauteur_image in range(0, hauteur, 8):
        for largeur_image in range(0, largeur, 8):
            bloc = []  # Créer une nouvelle matrice 8x8 pour chaque bloc
            for i in range(8):
                ligne = []
                for j in range(8):
                    if largeur_image + j < largeur and hauteur_image + i < hauteur:  # vérifie si il reste suffisament de pixels pour ajouter dans le blocs
                        ligne.append(matrice[hauteur_image + i][largeur_image + j])  # Ajouter le pixel à la ligne
                    else:
                        # ligne.append(0)
                        ligne.append(ligne[-1])  # si pas multiple de 8 on duplique les dernières valeurs
                bloc.append(ligne)  # Ajouter la ligne au bloc de 8x8
            matrice_blocs_8x8.append(np.array(bloc))  # Ajouter le bloc à la liste de blocs

    # Enregistrez les blocs dans un fichier texte
    with open('matrice_blocs_pixels.txt', 'w') as fichier:
        for bloc in matrice_blocs_8x8:
            fichier.write(np.array_str(bloc) + '\n\n')


matrice_quantification = [
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
]

#matrice qui sert juste à tester le code pour la quantification
matrice_apres_dct = [
    [-415.38, -30.19, -61.20, 27.24, 56.12, -20.10, -2.39, 0.46],
    [4.47, -21.86, -60.76, 10.25, 13.15, -7.09, -8.54, 4.88],
    [-46.83, 7.37, 77.13, -24.56, -28.91, 9.93, 5.42, -5.65],
    [-48.53, 12.07, 34.10, -14.76, -10.24, 6.3, 1.83, 1.95],
    [12.12, -6.55, -13.20, -3.95, -1.87, 1.75, -2.79, 3.14],
    [-7.73, 2.91, 2.38, -5.94, -2.38, 0.94, 4.30, 1.85],
    [-1.03, 0.18, 0.42, -2.42, -0.88, -3.02, 4.12, -0.66],
    [-0.17, 0.14, -1.07, -1.07, -1.17, -0.10, 0.50, 1.68]
]

def quantification(matrice):
    nouvelle_matrice_apres_quantification = []
    for i in range(len(matrice)):
        bloc = []
        for n in range (8):
            bloc.append(floor(matrice[i][n]/matrice_quantification[i][n]))
            nouvelle_matrice_apres_quantification.append(bloc)

    print(nouvelle_matrice_apres_quantification)
    return nouvelle_matrice_apres_quantification

#quantification(matrice_apres_dct)

if (__name__=='__main__'):
    decoupage8x8()
    print(quantification(matrice_apres_dct))
