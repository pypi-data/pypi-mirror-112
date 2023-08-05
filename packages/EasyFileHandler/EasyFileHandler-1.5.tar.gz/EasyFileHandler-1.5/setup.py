from setuptools import setup
from setuptools import find_packages

version = "1.5"

# This call to setup() does all the work
setup(
    name="EasyFileHandler",
    version=version,
    description="File Operations' Controller. Has Edit, Write(Format) And Read Features",
    url="https://github.com/v1s1t0r999/PyPi_Uploads/tree/EasyFileHandler",
    author="v1s1t0r999",
    author_email="aditya.funs.11@gmail.com",
    license="MIT",
    python_requires=">=3.6",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)