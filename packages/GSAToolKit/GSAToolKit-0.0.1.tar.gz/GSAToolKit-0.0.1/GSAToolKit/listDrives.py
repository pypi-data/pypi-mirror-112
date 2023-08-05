import os


def listDrives():
    return os.system("fsutil fsinfo drives")
