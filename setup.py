#   Jonathan Roth
#   jonathanroth@protonmail.com
#   https://github.com/JonathanRoth13
#   2022-03-03

from setuptools import setup, find_packages

setup(
    name="bumbling",
    version="0.1",
    license="MIT",
    author="Jonathan Roth",
    author_email="JonathanRoth@protonmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/JonathanRoth13/bumbling",
    install_requires=["PyExifTool"],
    entry_points={"console_scripts": ["bumbling=bumbling:main"]},
)
