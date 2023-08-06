import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PCA9685_wrapper",
    version="0.0.3",
    author="being24",
    author_email="being24@gmail.com",
    description="adafruit-pca9685 wrapper for Raspberry pi",
    install_requires=[
        "adafruit-pca9685",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/being24/PCA9685_Wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)