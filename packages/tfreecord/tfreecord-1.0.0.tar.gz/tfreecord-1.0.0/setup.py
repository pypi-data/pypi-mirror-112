import os

import pkg_resources
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="tfreecord",
    py_modules=["tfreecord", "tfrecords_pb2"],
    version="1.0.0",
    description="",
    author="Wikidepia",
    packages=find_packages(),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    url="https://github.com/Wikidepia/tfreecord",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
