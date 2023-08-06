import os

from setuptools import setup, find_packages


readme = os.path.join(os.path.dirname(__file__), "README.rst")

VERSION = '0.0.6'
DESCRIPTION = 'Systems are supposed to be tested'

setup(
    name="GSAToolKit",
    version=VERSION,
    author="Joe",
    author_email="alex.riddell88@gmail.com",
    description=DESCRIPTION,
    long_description=open(readme).read(),
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'GSA'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
