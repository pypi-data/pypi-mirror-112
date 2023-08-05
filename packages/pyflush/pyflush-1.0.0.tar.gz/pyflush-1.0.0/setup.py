import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyflush",
    version="1.0.0",
    author="Ravin Kumar",
    author_email="mr.ravin_kumar@hotmail.com",
    description="A python library to remove content of a directory, or file in a safer manner. After running pyflush, it became much safer to delete the file/directory manually/programmatically.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mr-ravin/pyflush",
    keywords = ['File Deletion', 'Deletion Utility', 'Directory Deletion','Delete Data','Data Deletion'],   # Keywords that define your package best
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
