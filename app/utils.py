from os import path

def getFullPath(relativePath):
    return path.abspath(path.join(path.dirname(__file__), relativePath))
