import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openapiparser-stigbd",  # Replace with your own username
    version="0.0.1",
    author="Stig B. Dørmænen",
    author_email="stigbd@gmail.com",
    description="A simple library to parse openAPI specs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Informasjonsforvaltning/openapiparser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
