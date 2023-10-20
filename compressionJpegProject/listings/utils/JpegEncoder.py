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
         

    def pictureToBinaryFile(self) -> str:
        """
            Turn a picture into a text file that represents its binary representation.
            @Return str == filename of the created file.
        """
        with open(self.picturePath,"rb") as readedFile:
            content = readedFile.readlines()
            writedFile = self.picturePath.split(".")[0]+"_RawBinaries.tx"
            with open(writedFile,"w") as wf:
                for line in content:
                    wf.write(line.hex())
            return writedFile


    @staticmethod
    def quantification(matrice,quantificationTable):
        return [[round(matrice[i][j]/quantificationTable[i][j]) for j in range(8)]for i in range(8)]

           
if __name__ == '__main__':
    owlBitmap = JpegEncoder("jpeg_picture_100px.jpg")
    bitmapPicture = JpegEncoder("bitmap_picture.bmp")
    print(owlBitmap.pictureFormat)
    print(bitmapPicture.pictureFormat)
    
    #Test quantification
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

    print(JpegEncoder.quantification(matrice_apres_dct,JpegEncoder.getQuantificationTable()))   

        
