import os


def treeDrives(drive="c:"):
    os.chdir(drive)
    return os.system("Tree /F")
