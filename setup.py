from setuptools import setup, find_packages

setup(
    name="thermal-monitor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pyserial',
    ],
) 