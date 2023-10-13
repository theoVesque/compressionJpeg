import PictureFileController

class BitmapController(PictureFileController):
    def __init__(self,fileName:str):
        if(BitmapController.isBitmapFile(fileName)):
            super().__init__(self,fileName)
        else:
            raise TypeError("Bad picture format: only bmp picture is accepted.")

    @staticmethod
    def isBitmapFile(fileName:str)->bool:
        """
            Test either the picture "fileName" is a bmp picture or not.
        """
        if(fileName.lower().split(".")[-1] == "bmp"):
            return True
        return False
