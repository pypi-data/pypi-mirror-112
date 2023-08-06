import os


def killChrome():
    os.system("taskkill /F /IM chrome.exe")
