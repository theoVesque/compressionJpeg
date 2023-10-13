from PictureFileController import *
from PIL import Image

class JpegController(PictureFileController):
    def __init__(self,fileName:str):
        if(JpegController.isJpegFile(fileName)):
            super().__init__(fileName)
            self.image = Image.open(self.picturePath)
        else:
            raise TypeError("Bad picture format: only jpeg picture is accepted.")

    @staticmethod
    def isJpegFile(fileName:str)->bool:
        """
            Test whether the picture "fileName" is a jpeg picture or not.
        """
        if(fileName.lower().split(".")[-1] in ["jpeg","jpe","jpg","jfif"]):
            return True
        return False
    
    
    def getPayloadData(self):
        if(self.image):
            return self.image.getdata()
        else:
            return ValueError("\"image\" attribut is not defined.")


if __name__ == '__main__':
    jpegC = JpegController("jpeg_picture.jpg")
    print(jpegC.getPayloadData())