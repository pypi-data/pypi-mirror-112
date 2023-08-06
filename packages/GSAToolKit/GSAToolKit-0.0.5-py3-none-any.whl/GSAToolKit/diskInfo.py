import os


def diskInfo(disk="c:"):
    os.system(disk)
    return os.system("wmic diskdrive list full")
