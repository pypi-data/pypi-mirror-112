import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycalil",
    version="1.0",
    author="warada0209",
    author_email="warada0209@gmail.com",
    description="A package that enables the Calil Library API to be used from Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/warada0209/pycalil",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)