from functions import *
from PIL import Image
import numpy as np

class JpegEncoder():
    """
        Class that allows to encode PNG or Bitmap picture into JFIF format (JPEG Compression)
    """
    def __init__(self, pictureFile:str):
            self.picturePath = getAbsPicturePath(pictureFile)
            self.image = Image.open(self.picturePath)
            self.pictureFormat = self.image.format


    def isBitmapFile(self)->bool:
        """
            Test either the picture "fileName" is a bmp picture or not.
        """
        return (self.pictureFormat == "BMP")
    

    def isPngFile(self)->bool:
        """
            Test either the picture "fileName" is a png picture or not.
        """
        return (self.pictureFormat == "PNG")


    @staticmethod
    def getQuantificationTable():
        return [
                [16, 11, 10, 16, 24, 40, 51, 61],
                [12, 12, 14, 19, 26, 58, 60, 55],
                [14, 13, 16, 24, 40, 57, 69, 56],
                [14, 17, 22, 29, 51, 87, 80, 62],
                [18, 22, 37, 56, 68, 109, 103, 77],
                [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101],
                [72, 92, 95, 98, 112, 100, 103, 99]
                ]

    @staticmethod
    def quantification(matrice,quantificationTable):
        return [[round(matrice[i][j]/quantificationTable[i][j]) for j in range(8)]for i in range(8)]
    
    def getPixelsMatrix(self):
        if(self.image):
            listOfPixels = list(self.image.getdata())
            width,height = self.image.size
            l=0
            c=0
            k=0
            matrixOfPixels = []
            while l < height :
                ligne = []
                while c < width:
                    ligne.append(listOfPixels[c+k])
                    c+=1
                matrixOfPixels.append(ligne)
                c=0
                k+=width
                l+=1
            return matrixOfPixels
        else:
            return ValueError("\"image\" attribut is not defined.")

    def adjustSizeOfMatrixOfPixels_repeatEnd(self):
        width,height = self.image.size
        matrixOfPixels = self.getPixelsMatrix()
        nbOfPixelsToAddPerline = 8 - width%8
        nbOfPixelsToAddPerCol = 8 - height%8
        for l in range (len(matrixOfPixels)):
            matrixOfPixels[l] = matrixOfPixels[l] + matrixOfPixels[l][-nbOfPixelsToAddPerline::]
        matrixOfPixels = matrixOfPixels + matrixOfPixels[-nbOfPixelsToAddPerCol::]
        return matrixOfPixels
    
    def adjustSizeOfMatrixOfPixels_addWhitePixels(self):
        width,height = self.image.size
        matrixOfPixels = self.getPixelsMatrix()
        nbOfPixelsToAddPerline = 8 - width%8
        nbOfPixelsToAddPerCol = 8 - height%8
        for l in range (len(matrixOfPixels)):
            matrixOfPixels[l] = matrixOfPixels[l] + [255]*nbOfPixelsToAddPerline
        matrixOfPixels = matrixOfPixels + [[255]*len(matrixOfPixels[0])]*nbOfPixelsToAddPerCol
        return matrixOfPixels
    
    def createPictureFromMatrixOfPixels(self,type):
        if(type.upper()=="RP"):
            adjustedPictureMatrixOfPixels = self.adjustSizeOfMatrixOfPixels_repeatEnd()
        elif(type.upper()=="WP"):
            adjustedPictureMatrixOfPixels = self.adjustSizeOfMatrixOfPixels_addWhitePixels()
        else:
            raise Exception("Type attribut is unknown")

        adjustedPictureListOfPixels = []
        
        #Transform matrix of pixels to list of pixels
        for l in range(len(adjustedPictureMatrixOfPixels)):
            for c in range(len(adjustedPictureMatrixOfPixels[0])):
                adjustedPictureListOfPixels.append(adjustedPictureMatrixOfPixels[l][c])
        
        #Creating the new picture with adjusted size
        width = len(adjustedPictureMatrixOfPixels[0])
        height = len(adjustedPictureMatrixOfPixels)
        adjustedPicture = Image.new("L",(width,height))
        adjustedPicture.putdata(adjustedPictureListOfPixels)
        adjustedPicture.save(self.picturePath+"_adjusted.bmp")

    def decoupage8x8(self,adjustedMatrixOfPixels):
        #Dimenssion des matrices utilisées
        matrixHeight = len(adjustedMatrixOfPixels)
        matrixWidth = len(adjustedMatrixOfPixels[0])
        widthMatrixOfBlocks = matrixWidth//8
        heightMatrixOfBlocks = matrixHeight//8
        matrixOfBlocks = []
        #Création d'une matrice de blocks vides
        for _ in range(heightMatrixOfBlocks):
            matrixOfBlocks.append([])
            for _ in range(widthMatrixOfBlocks):
                matrixOfBlocks[-1].append([[],[],[],[],[],[],[],[]])
        #Insertion des valeurs dans la matrice
        indiceLigneBlock = 0
        for l in range(matrixHeight):
            for c in range(matrixWidth):
                if (len(matrixOfBlocks[l//8][c//8][indiceLigneBlock]) == 8 ):
                    indiceLigneBlock += 1
                matrixOfBlocks[l//8][c//8][indiceLigneBlock].append(adjustedMatrixOfPixels[l][c])
                if(indiceLigneBlock == 7 and len(matrixOfBlocks[l//8][widthMatrixOfBlocks-1][indiceLigneBlock]) == 8):
                    indiceLigneBlock = 0
        return matrixOfBlocks

    def parcoursZigZag():      
        
if __name__ == '__main__':
    owlBitmap = JpegEncoder("bitmap_picture_250.bmp")
    print(owlBitmap.pictureFormat)
    owlBitmap.image = owlBitmap.image.convert('L')
    #print(owlBitmap.getPixelsMatrix())
    #matrix = owlBitmap.adjustSizeOfMatrixOfPixels_addWhitePixels()
    owlBitmap.createPictureFromMatrixOfPixels("wp")
    owlBitmapMatrixOfPixel = owlBitmap.adjustSizeOfMatrixOfPixels_addWhitePixels()
    print(owlBitmap.decoupage8x8(owlBitmapMatrixOfPixel))

    """ matrice_test_decoupage = [
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8],
    ] """
    #print(owlBitmap.decoupage8x8(matrice_test_decoupage))
    

    
    #Test quantification
    #matrice qui sert juste à tester le code pour la quantification
    """ matrice_apres_dct = [
        [-415.38, -30.19, -61.20, 27.24, 56.12, -20.10, -2.39, 0.46],
        [4.47, -21.86, -60.76, 10.25, 13.15, -7.09, -8.54, 4.88],
        [-46.83, 7.37, 77.13, -24.56, -28.91, 9.93, 5.42, -5.65],
        [-48.53, 12.07, 34.10, -14.76, -10.24, 6.3, 1.83, 1.95],
        [12.12, -6.55, -13.20, -3.95, -1.87, 1.75, -2.79, 3.14],
        [-7.73, 2.91, 2.38, -5.94, -2.38, 0.94, 4.30, 1.85],
        [-1.03, 0.18, 0.42, -2.42, -0.88, -3.02, 4.12, -0.66],
        [-0.17, 0.14, -1.07, -1.07, -1.17, -0.10, 0.50, 1.68]
    ]

    print(JpegEncoder.quantification(matrice_apres_dct,JpegEncoder.getQuantificationTable()))    """

        
