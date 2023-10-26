from os import path, getcwd
import numpy as np

def getAbsPicturePath(pictureFileName:str):
    relativePath = f"compressionJpegProject\\listings\\static\\pictures\\{pictureFileName}"
    res = path.join(getcwd(),relativePath)
    return res

def pictureToBinaryFile(picturePath:str) -> str:
    """
        Turn a picture into a text file that represents its binary representation.
        @Return str == filename of the created file.
    """
    with open(picturePath,"rb") as readedFile:
        content = readedFile.readlines()
        writedFile = picturePath.split(".")[0]+"_RawBinaries.tx"
        with open(writedFile,"w") as wf:
            for line in content:
                wf.write(line.hex())
        return writedFile
    
def afficherMatrice(matrice):
    for ligne in matrice:
        print(ligne)

def npArrayToPyhtonList(array:np.array):
        lignes,colonnes = array.shape
        matricePython = []
        for i in range(lignes):
            matricePython.append([])
            for j in range(colonnes):
                matricePython[-1].append(round(array[i, j],2))
        return matricePython