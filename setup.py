from setuptools import setup, find_packages

setup(
    name="awesome-actus-lib",
    version="1.0.0",
    description="Modular Python Package for Financial Contract Modelling with the ACTUS Standard",
    author="maierdon",
    author_email="whyaxis21@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
)