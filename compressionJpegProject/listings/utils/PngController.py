import PictureFileController

class PngController(PictureFileController):
    def __init__(self,fileName:str):
        if(PngController.isPngFile(fileName)):
            super().__init__(self,fileName)
        else:
            raise TypeError("Bad picture format: only png picture is accepted.")

    @staticmethod
    def isPngFile(fileName:str)->bool:
        """
            Test either the picture "fileName" is a png picture or not.
        """
        if(fileName.lower().split(".")[-1] == "png"):
            return True
        return False

