from os import path, getcwd

class PictureFileController:
    def __init__(self, pictureFile:str):
            self.picturePath = PictureFileController.getAbsPicturePath(pictureFile)
            self.pictureFormat = pictureFile.split(".")[-1]

    @staticmethod
    def getAbsPicturePath(pictureFileName:str):
        relativePath = f"listings/static/pictures/{pictureFileName}"
        return path.join(getcwd(),relativePath)

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


if __name__ == '__main__':
    print(PictureFileController.getAbsPicturePath("jpeg_picture.jpg"))
        


