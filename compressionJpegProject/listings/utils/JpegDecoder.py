from functions import *
from PIL import Image

class JpegDecoder():
    def __init__(self,fileName:str):
        self.picturePath = getAbsPicturePath(fileName)
        self.image = Image.open(self.picturePath)
        self.pictureFormat = self.image.format

    def isJpegFile(fileName:str)->bool:
        """
            Test whether the picture "fileName" is a jpeg picture or not.
        """
        if(fileName.lower().split(".")[-1] in ["jpeg","jpe","jpg","jfif"]):
            return True
        return False
    
    def getPixelsMatrix(self):
        if(self.image):
            return list(self.image.getdata())
        else:
            return ValueError("\"image\" attribut is not defined.")
    
    def getCompressedDataFromJpegPicture(self):
        if(self.image):
            return self.image.tobytes()
        else:
            return ValueError("\"image\" attribut is not defined.")
        
    def writeDataToFile(self,nameFile:str)->bool:
        filePath = getAbsPicturePath(nameFile)
        print(filePath)
        with open(filePath,'w') as writedFile:
            data = self.getCompressedDataFromJpegPicture()
            writedFile.write(data.hex())
        if path.isfile(filePath):
            return True
        else :
            return False

    def convertPictureData(self,pixelMode:str):
        if(self.image):
            self.image.convert(pixelMode)
        else:
            return ValueError("\"image\" attribut is not defined.")

if __name__ == '__main__':
    owlJpeg = JpegDecoder("jpeg_picture_100px.jpg")
    owlJpeg.convertPictureData("L")
    print(owlJpeg.getCompressedDataFromJpegPicture())
    owlJpeg.writeDataToFile("jpeg_picture_100px_binaries.txt")
    pictureToBinaryFile(owlJpeg.picturePath)
    
