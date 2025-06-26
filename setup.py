from setuptools import setup, find_packages

setup(
    name="awesome_actus_lib",
    version="0.1.0",
    packages=find_packages(include=["awesome_actus_lib", "awesome_actus_lib.*"]),
    install_requires=[],
)
