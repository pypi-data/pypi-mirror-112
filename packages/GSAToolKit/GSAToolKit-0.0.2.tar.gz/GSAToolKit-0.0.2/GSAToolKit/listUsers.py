import os


def listUsers():
    os.chdir("C:/Users")
    return os.system("dir")
