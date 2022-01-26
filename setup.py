from setuptools import setup, find_packages

setup(
name="bumbling"
version="0.1"
author="Jonathan Roth"
author_email="JonathanRoth@protonmail.com"
packages=find_packages()
#scripts=["bumbling.py" ]
entry_points={
        'console_scripts': ['bumbling'=bumbling:main]
    }
install_requires=["PyExifTool"]
url="https://github.com/JonathanRoth13/bumbling"
)
