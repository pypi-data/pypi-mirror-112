import psutil
import os


def killNetSupport():
    apps = ["StudentUI.exe", "NSSilence.exe", "Runplugin64.exe", "runplugin.exe"]
    for app in apps:
        for proc in psutil.process_iter():
            try:
                if app.lower() in proc.name().lower():
                    os.system("taskkill /F /IM {}".format(app))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        print("{} is not running".format(app))
