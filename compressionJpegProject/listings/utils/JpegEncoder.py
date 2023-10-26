from functions import *
from PIL import Image
from math import cos, pi, sqrt
from copy import deepcopy
from collections import Counter
from huffmanEncoding import *

class JpegEncoder():
    """
        Class that allows to encode PNG or Bitmap picture into JFIF format (JPEG Compression)
    """
    def __init__(self, pictureFile:str):
            self.picturePath = getAbsPicturePath(pictureFile)
            self.image = Image.open(self.picturePath)
            self.pictureFormat = self.image.format
            self.width , self.height = self.image.size

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
        
    @staticmethod
    def calculDCTvalue(bloc8x8,u,v)->float:
        dctValue:np.float64 = 0.0
        cu = 1 / sqrt(2) if (u == 0) else 1  
        cv = 1 / sqrt(2) if (v == 0) else 1
        for l in range(len(bloc8x8)):
            for c in range(len(bloc8x8[0])):
                centeredValue = bloc8x8[l][c] - 128
                dctValue += \
                    np.float64(0.25 * cu * cv * centeredValue \
                    * cos((2 * l + 1 ) * u * pi / 16) \
                    * cos((2 * c + 1 ) * v * pi / 16))
        return dctValue
    
    @staticmethod
    def DCT8x8(block8x8:np.array): 
        N, _= block8x8.shape
        matriceDCT = np.zeros((N,N))
        for u in range(N):
            for v in range(N):
                matriceDCT[u, v] = JpegEncoder.calculDCTvalue(block8x8,u,v)
        return matriceDCT


    @staticmethod
    def matrixtoList(blockMatrix):
        resultat = []
        for lb in range(len(blockMatrix)):
            for cb in range(len(blockMatrix[0])):
                resultat.append(blockMatrix[lb][cb])
        return resultat

    
    @staticmethod
    def zigZag(matrice):
        lignes = len(matrice)
        colonnes = len(matrice[0])
        listezigZag = []
        i=0
        j=0
        while(i<=lignes-1 and j<=colonnes-1):
            listezigZag.append(matrice[i][j])
            if(i==0 or i==lignes-1):
                if(j==colonnes-1):
                    j-=1
                    i+=1
                j+=1
                listezigZag.append(matrice[i][j])
            else:
                if j == 0 or j == colonnes-1:
                    if i == lignes-1:
                        i = i - 1
                        j = j + 1
                    i = i + 1
                    listezigZag.append(matrice[i][j])
            if i == 0 or j == colonnes-1:
                limit = False
            if j == 0 or i == lignes-1:
                limit = True
            if limit:
                i = i - 1
                j = j + 1
            else:
                i = i + 1
                j = j - 1
        return listezigZag
    
    @staticmethod
    def RLE(zigzag):
        resultat = []  # Tuple pour stocker les valeurs resultat
        compteur = 1  # On intialise un compteur
        valeur_precedente = zigzag[0]

        for i in range(1, len(zigzag)):
            valeur_actuelle = zigzag[i]
            if valeur_actuelle == valeur_precedente:
                compteur += 1
            else:
                resultat.append((valeur_precedente, compteur))
                compteur = 1
                valeur_precedente = valeur_actuelle

        resultat.append((valeur_precedente, compteur)) # Ajoute le dernier resultat
        return resultat
    
    def JPEGCompression(self) -> (str, any):
        #On récupère la matrice de pixels de l'image
        matrixPixels = self.adjustSizeOfMatrixOfPixels_addWhitePixels()
        blocksMatrix = self.decoupage8x8(matrixPixels)
        blockMatrixDCTQuantified = deepcopy(blocksMatrix)
        for lb in range(len(blocksMatrix)):
            for cb in range(len(blocksMatrix[0])):
                blockMatrixDCTQuantified[lb][cb] = JpegEncoder.quantification(npArrayToPyhtonList(JpegEncoder.DCT8x8(np.array(blocksMatrix[lb][cb]))),JpegEncoder.getQuantificationTable())
        dataZigZagScanningMatrix = []
        for lb in range(len(blocksMatrix)):
            for cb in range(len(blocksMatrix[0])):
                dataZigZagScanningMatrix.append(JpegEncoder.zigZag( blockMatrixDCTQuantified[lb][cb]))
        dataZigZagScanning = JpegEncoder.matrixtoList(dataZigZagScanningMatrix)
        #Encodage RLE
        dataRLE = JpegEncoder.RLE(dataZigZagScanning)
        #Encodage Huffman
        return Huffman_Encoding(dataRLE)


    
if __name__ == '__main__':
    #print(owlBitmap.decoupage8x8(owlBitmapMatrixOfPixel))

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
        [1,2,2,1,3,1,1,1,9,1,1,1,2,3,4,8]
    ] """
    #print(owlBitmap.decoupage8x8(matrice_test_decoupage))
    #Test centrage d'une matrice
    matrice_test_dct = [
        [52, 55, 61, 66, 70, 61, 64, 73],
        [63, 59, 55, 90, 109, 85, 69, 72],
        [62, 59, 68, 113, 144, 104, 66, 73],
        [63, 58, 71, 122, 154, 106, 70, 69],
        [67, 61, 68, 104, 126, 88, 68, 70],
        [79, 65, 60, 70, 77, 68, 58, 75],
        [85, 71, 64, 59, 55, 61, 65, 83],
        [87, 79, 69, 87, 65, 76, 78, 94]
    ]

    array_test_dct = np.array([[52, 55, 61, 66, 70, 61, 64, 73],
            [63, 59, 55, 90, 109, 85, 69, 72],
            [62, 59, 68, 113, 144, 104, 66, 73],
            [63, 58, 71, 122, 154, 106, 70, 69],
            [67, 61, 68, 104, 126, 88, 68, 70],
            [79, 65, 60, 70, 77, 68, 58, 75],
            [85, 71, 64, 59, 55, 61, 65, 83],
            [87, 79, 69, 68, 65, 76, 78, 94]])
    #Test matriceDCT

    arrayDCT = JpegEncoder.DCT8x8(array_test_dct)  
    matriceDCT = npArrayToPyhtonList(arrayDCT)
    
    print("**************** Original Matrix Blocks 8x8 ****************") 
    afficherMatrice(matrice_test_dct)
    print()
    
    print("**************** DCT Matrix ****************") 
    afficherMatrice(matriceDCT)
    print()
    
    #Test quantification
    quantifiedMatrix = JpegEncoder.quantification(matriceDCT,JpegEncoder.getQuantificationTable())

    print("**************** Data after ZigZag Scanning ****************")
    zigZagMatrix = JpegEncoder.zigZag(quantifiedMatrix)
    print(zigZagMatrix)
    print()

    dataRLE = JpegEncoder.RLE(zigZagMatrix)
    print("**************** Binary Data after RLE Encoding ****************")
    print(dataRLE)
    print() 

    # Exemple d'utilisation
    huffman_binaries,huffmanTree = Huffman_Encoding(dataRLE)

    print("**************** Binary Data after Huffman Encoding ****************")
    print(huffman_binaries)
    print()

    """ decoded_data_huffman = Huffman_Decoding(huffman_binaries,huffmanTree)

    print("**************** Decoded Data *****************")
    print(decoded_data_huffman)
    print() """
    
    #Test avec un vrai image
    owlBitmap = JpegEncoder("bitmap_picture.bmp")
    #print(owlBitmap.pictureFormat)
    owlBitmap.image = owlBitmap.image.convert('L')
    #print(owlBitmap.getPixelsMatrix())
    #matrix = owlBitmap.adjustSizeOfMatrixOfPixels_addWhitePixels()
    owlBitmap.createPictureFromMatrixOfPixels("wp")
    owlBitmapMatrixOfPixel = owlBitmap.adjustSizeOfMatrixOfPixels_addWhitePixels()
    print("Width = ",owlBitmap.width)
    print("Height = ",owlBitmap.height)
    owlBitmap.JPEGCompression()
    


        
