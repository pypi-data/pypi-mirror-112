from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="metrc-client-python",
    version="0.0.1",
    author="Jesse Freeman",
    author_email="jessewilliamfreeman@gmail.com",
    description="Python client library for accessing the Metrc API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jessewilliamfreeman/metrc-python",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'requests'
    ],
    packages=find_packages(exclude='example'),
    python_requires=">=3.6",
)