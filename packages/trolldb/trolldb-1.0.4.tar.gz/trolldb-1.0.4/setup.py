import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="trolldb",
    version="1.0.4",
    description="JSON Database but just encrypted",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ProYT303/trollDB",
    author="Walterepic",
    author_email="social.proyt303@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["cryptography"],
    include_package_data=True,
)