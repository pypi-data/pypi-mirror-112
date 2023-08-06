import pathlib
from setuptools import setup

# Directory of this file
HERE = pathlib.Path(__file__).parent

# Text of the README file
README = HERE.joinpath("README.md").read_text()

# This is the call which does all the work
setup(
    name="smartetailing",
    version="0.4.5",
    description="Connect to the smartetailing website order feeds",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/fundthmcalculus/smartetailing",
    author="Scott Phillips",
    author_email="polygonguru@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8"
    ],
    packages=["smartetailing"],
    include_package_data=True,
    install_requires=["lxml", "requests", "urllib3", "beautifulsoup4", "pyap"]
)