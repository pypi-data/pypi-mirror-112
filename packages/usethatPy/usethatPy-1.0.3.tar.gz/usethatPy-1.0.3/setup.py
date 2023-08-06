import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="usethatPy",
    version="1.0.3",
    author="jixing",
    author_email="jixing475@163.com",
    description="A small demo package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jixing475/usethatPy",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
