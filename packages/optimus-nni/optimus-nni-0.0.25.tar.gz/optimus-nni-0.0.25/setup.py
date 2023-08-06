import os
import sys
import warnings

from setuptools import setup

if sys.version_info <= (2, 7):
    warnings.warn(
        "Python 2.7 is no longer supported." " Please upgrade to Python 3.5+ .", DeprecationWarning
    )

VERSION = '0.0.25'

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "requirements.txt")) as requirements_fp:
    install_requires = requirements_fp.read().split("\n")

setup(
    name="optimus-nni",
    version=VERSION,
    description="Optimus NNI Extension",
    author="unianalysis",
    author_email="contact@unianalysis.com",
    url="https://aiexcelsior.art/",
    packages=["optimus_nni"],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
