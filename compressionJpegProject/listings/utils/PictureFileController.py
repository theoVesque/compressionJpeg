from os import path,getcwd
from abc import ABC

class PictureFileController(ABC):
    def __init__(self, pictureFile:str):
            self.picturePath = PictureFileController.getAbsPicturePath(pictureFile)
            self.pictureFormat = pictureFile.split(".")[-1]

    @staticmethod
    def getAbsPicturePath(pictureFileName:str):
        relativePath = f"compressionJpegProject\\listings\\static\\pictures\\{pictureFileName}"
        res = path.join(getcwd(),relativePath)
        return res
    
    def isGoodFileFormat(fileName:str)
         

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
        
    
        
    
    




if __name__ == '__main__':
    myPath = PictureFileController.getAbsPicturePath("jpeg_picture.jpg")
    print(getcwd())
    print(myPath)
    print(path.exists(myPath))
        


