import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="refkeys",
    version="0.0.2",
    author="Ravin Kumar",
    author_email="mr.ravin_kumar@hotmail.com",
    description="This repository contains a tool for secret-sharing among two parties.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mr-ravin/refkeys",
    keywords = ['Secret Sharing', 'Cryptography', 'Security Tools','Secret Key','Secret Key Generation'],   # Keywords that define your package best
    install_requires=[        
      ],

    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
