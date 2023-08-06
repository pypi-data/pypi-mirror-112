
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="habcatev",
    version="0.0.1",
    author="HabCat team",
    author_email="",
    description="Librería para la gestión de eventos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alpeza/habcatev",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 
