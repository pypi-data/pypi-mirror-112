import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyargus",
    version="1.1.post1",
    author="Tamas Peto",
    author_email="petotax@gmail.com",
    description="Signal processing algorithms for antenna arrays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/petotamas/pyArgus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering"
    ],
)
