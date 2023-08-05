from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='pingdiscover',
    version='1.1.1',
     description = 'A simple commandline app for ip lookup with concurrent processes',
     python_requires='>=3.7',
     author="Ilkin Mammadov",
     long_description=README,
     long_description_content_type="text/markdown",
     license='MIT',
      author_email='ilkma1998@gmail.com',
      classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
        ],
    packages=find_packages(include=['src', 'src.*', '.']),
    install_requires=[
         'aiodns==3.0.0',
         'aioping==0.3.1',
         'async-timeout==3.0.1',
         'cffi==1.14.5',
         'pycares==4.0.0',
         'pycparser==2.20' 
      ],
    entry_points={
        'console_scripts': ['pingdiscover=src.pingdiscover:main']
    },
)




