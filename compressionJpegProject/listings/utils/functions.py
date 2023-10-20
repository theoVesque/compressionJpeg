from os import path, getcwd

def getAbsPicturePath(pictureFileName:str):
    relativePath = f"compressionJpegProject\\listings\\static\\pictures\\{pictureFileName}"
    res = path.join(getcwd(),relativePath)
    return res

def pictureToBinaryFile(picturePath:str) -> str:
    """
        Turn a picture into a text file that represents its binary representation.
        @Return str == filename of the created file.
    """
    with open(picturePath,"rb") as readedFile:
        content = readedFile.readlines()
        writedFile = picturePath.split(".")[0]+"_RawBinaries.tx"
        with open(writedFile,"w") as wf:
            for line in content:
                wf.write(line.hex())
        return writedFile