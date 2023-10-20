from PictureFileController import *
import os.path

class JpegController(PictureFileController):
    def __init__(self,fileName:str):
        if(JpegController.isJpegFile(fileName)):
            super().__init__(fileName)
            self.image = Image.open(self.picturePath)
        else:
            raise TypeError("Bad picture format: only jpeg picture is accepted.")

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
        filePath = self.getAbsPicturePath(nameFile)
        print(filePath)
        with open(filePath,'w') as writedFile:
            data = self.getCompressedDataFromJpegPicture()
            writedFile.write(data.hex())
        if os.path.isfile(filePath):
            return True
        else :
            return False

    def convertPictureData(self,pixelMode:str):
        if(self.image):
            self.image.convert(pixelMode)
        else:
            return ValueError("\"image\" attribut is not defined.")

if __name__ == '__main__':
    owlJpeg = JpegController("jpeg_picture_100px.jpg")
    owlJpeg.convertPictureData("L")
    print(owlJpeg.getCompressedDataFromJpegPicture())
    owlJpeg.writeDataToFile("jpeg_picture_100px_binaries.txt")
    owlJpeg.pictureToBinaryFile()
    
