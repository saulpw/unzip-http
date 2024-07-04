# SPDX-License-Identifier: MIT

from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()

def requirements():
    with open("requirements.txt") as f:
        return f.read().split("\n")


setup(
        name="unzip-http",
        version="0.5.1",
        description="extract files from .zip files over http without downloading entire archive",
        long_description=readme(),
        long_description_content_type="text/markdown",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3",
        ],
        keywords="http zip unzip",
        author="Saul Pwanson",
        url="https://github.com/saulpw/unzip-http",
        python_requires=">=3.8",
        py_modules=["unzip_http"],
        scripts=["unzip-http"],
        install_requires=requirements(),
)
