class PictureFileController:
    def __init__(self,pictureFile:str):
        if(PictureFileController.isJpegFile(pictureFile)
           or PictureFileController.isBitmapFile(pictureFile)
           or PictureFileController.isPngFile(pictureFile)):
            self.pictureFile = pictureFile
            self.pictureFormat = pictureFile.split(".")[-1]
        else:
            raise Exception("File format of your picture is not valid. Only PNG, JPEG or BMP format are accepted !")

    @staticmethod
    def isJpegFile(fileName:str)->bool:
        if(fileName.lower().split(".")[-1] in ["jpeg","jpe","jpg","jfif"]):
            return True
        return False
    
    @staticmethod
    def isBitmapFile(fileName:str)->bool:
        if(fileName.lower().split(".")[-1] == "bmp"):
            return True
        return False
    
    @staticmethod
    def isPngFile(fileName:str)->bool:
        if(fileName.lower().split(".")[-1] == "png"):
            return True
        return False
   
    def pictureToBinaryFile(self) -> str:
        """
            Turn a picture into a text file that represents its binary representation.
        """
        with open(self.pictureFile,"rb") as readedFile:
            content = readedFile.readlines()
            writedFile = self.pictureFile.split(".")[0]+"_binaries.tx"
            with open(writedFile,"w") as wf:
                for line in content:
                    wf.write(line.hex())
            return writedFile

            

if __name__ == '__main__':
    pictureC = PictureFileController("compressionJpeg/listings/static/pictures/bitmap_picture.jpg")
    pictureC.pictureToBinaryFileBinaryFile()
        


