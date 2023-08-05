import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ravdec",
    version="1.3",
    author="Ravin Kumar",
    author_email="mr.ravin_kumar@hotmail.com",
    description="Lossless Data Compression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/mr-ravin/ravdec",
    keywords = ['Data Compression', 'Lossless Data Compression', 'Compression','Lossless Compression'],   # Keywords that define your package best
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

