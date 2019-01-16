# coding: utf8
import os
import io
import re

from setuptools import find_packages, setup

CWD = os.path.dirname(os.path.abspath(__file__))

about = {}
with open(os.path.join(CWD, 'python12306', '__version__.py')) as f:
    exec(f.read(), about)

with io.open("README.md", 'r', encoding='utf8') as f:
    long_description = re.sub(r':\w+:\s', '', f.read())  # Remove emojis

setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", )),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.5",
    install_requires=[
        "requests",
        "Pillow",
        "PrettyTable",
        "colorama",
        "namedtupled",
        "PyYAML",
        "cached-property"
    ],
    entry_points={
        "console_scripts": {
            "py12306 = python12306.cmd:main"
        },
    },

    classifiers=[
        "Programming Language :: Python :: 3.5"
        "Programming Language :: Python :: 3.6"
        "Programming Language :: Python :: 3.7"
    ],
)
