from setuptools import find_packages, setup

setup(
    name="colorconversion",
    version="0.1.2",
    description="converts images from one color table to another",
    author="Mathieu Moalic",
    author_email="matmoa@pm.me",
    platforms=["any"],
    license="GPL-3.0",
    url="https://github.com/MathieuMoalic/colorconversion",
    packages=find_packages(),
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
)
