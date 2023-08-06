import setuptools
from pathlib import Path

setuptools.setup(
    name="tucpdf",
    version=2.0,
    description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["data", "tests"])
)
