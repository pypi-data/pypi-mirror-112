import os


def installPythonModule(python_module):
    return os.system("pip install {}".format(python_module))
