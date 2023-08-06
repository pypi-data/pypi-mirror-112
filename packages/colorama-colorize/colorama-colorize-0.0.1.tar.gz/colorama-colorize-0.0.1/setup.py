from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Better syntax for Colorama'
LONG_DESCRIPTION = 'A package that allows you to use the colorama module with a simpler syntax'

# Setting up
setup(
    name="colorama-colorize",
    version=VERSION,
    author="Rikai",
    author_email="rikai@rikaisan.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['colorama'],
    keywords=['python', 'color', 'easy', 'colorize', 'better'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)