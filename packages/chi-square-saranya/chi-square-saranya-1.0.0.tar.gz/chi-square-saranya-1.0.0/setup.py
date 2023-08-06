import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="chi-square-saranya",
    version="1.0.0",
    description="It Outputs if the required categorical column is dependent or independent of output categorical column",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/saranya-sekar/chi-square-saranya",
	download_url = "https://github.com/saranya-sekar/chi-square-saranya/archive/refs/tags/final-01.tar.gz",
    author="Saranya Sekar",
    author_email="saranyatagore@yahoo.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["chi-square-saranya"],
    include_package_data=True,
    install_requires=[],
    
    
)
