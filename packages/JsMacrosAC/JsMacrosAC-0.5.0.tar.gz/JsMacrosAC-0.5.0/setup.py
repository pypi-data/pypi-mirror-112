from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


VERSION = '0.5.0'
DESCRIPTION = 'A package to let your IDE know what JsMacros can do'

# Setting up
setup(
    name="JsMacrosAC",
    version=VERSION,
    author="Hasenzahn1",
    author_email="<motzer10@gmx.de>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'JsMacros', 'Autocomplete', 'Doc'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)