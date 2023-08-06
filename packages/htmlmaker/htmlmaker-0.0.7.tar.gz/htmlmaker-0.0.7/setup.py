import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="htmlmaker",
    version="0.0.7",
    author="tsdm",
    author_email="tsdmtsdm@126.com",
    description="Package for create html from data quickly.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.tsdm39.net",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)