from os import path

def getFullPath(relativePath):
    return path.abspath(path.join(path.dirname(__file__), relativePath))

def getVersion():
    with open(getFullPath("version")) as file:
        return file.readline()
