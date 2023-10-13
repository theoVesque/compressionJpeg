class PictureFileController:
    def __init__(self,pictureFile:str):
            self.pictureFile = pictureFile
            self.pictureFormat = pictureFile.split(".")[-1]
        
    def pictureToBinaryFile(self) -> str:
        """
            Turn a picture into a text file that represents its binary representation.
            @Return str == filename of the created file.
        """
        with open(self.pictureFile,"rb") as readedFile:
            content = readedFile.readlines()
            writedFile = self.pictureFile.split(".")[0]+"_binaries.tx"
            with open(writedFile,"w") as wf:
                for line in content:
                    wf.write(line.hex())
            return writedFile

    
        


