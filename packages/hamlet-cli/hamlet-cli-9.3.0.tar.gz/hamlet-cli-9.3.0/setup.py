from setuptools import setup
import os

VERSION = "9.3.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="hamlet-cli",
    description="hamlet-cli is now hamlet",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["hamlet"],
    classifiers=["Development Status :: 7 - Inactive"],
    author='Hamlet',
    author_email='help@hamlet.io',
    url='https://hamlet.io'
)
