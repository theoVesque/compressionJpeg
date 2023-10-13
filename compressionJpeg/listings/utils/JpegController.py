import PictureFileController

class JpegController(PictureFileController):
    def __init__(self,fileName:str):
        if(JpegController.isJpegFile(fileName)):
            super().__init__(self,fileName)
        else:
            raise TypeError("Bad picture format: only jpeg picture is accepted.")

    @staticmethod
    def isJpegFile(fileName:str)->bool:
        """
            Test either the picture "fileName" is a jpeg picture or not.
        """
        if(fileName.lower().split(".")[-1] in ["jpeg","jpe","jpg","jfif"]):
            return True
        return False
