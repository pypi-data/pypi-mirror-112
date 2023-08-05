import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qrandom",
    version="0.7",
    author="Ravin Kumar",
    author_email="mr.ravin_kumar@hotmail.com",
    description="This repository contains the source code of research paper titled: \" A generalized quantum algorithm for assuring fairness in random selection among 2^n participants\"",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mr-ravin/QrandomSelection",
    keywords = ['Quantum Algorithm','Quantum Fairness', 'One to One', 'Quantum Random Number','Random Selection','Lucky Draw'],   # Keywords that define your package best
    install_requires=['qiskit'        
      ],

    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


