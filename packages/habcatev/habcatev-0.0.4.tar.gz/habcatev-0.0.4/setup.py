
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="habcatev",
    version="0.0.4",
    author="HabCat Team",
    author_email="",
    description="Librería para la gestión de eventos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alpeza/habcatev",
    packages=setuptools.find_packages(),
    install_requires=[
        'paho_mqtt==1.5.1',
        'PyYAML==5.4.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 



