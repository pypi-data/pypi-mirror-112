import setuptools
from pathlib import Path

setuptools.setup(
    name="zakpdf",
    version=1.0,
    long_discription=Path("README.md").read_text(),
    package=setuptools.find_packages(exclude=["test", "data"])
)
