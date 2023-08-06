import pathlib
from setuptools import find_packages, setup
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="bbc-reader",
    version="1.0.4",
    description="Read the latest BBC news",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Khang Nguyen",
    author_email="khangvu.1109@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['BBC'],
    include_package_data=True,
    install_requires=["feedparser", "html2text"],
    entry_points={
        "console_scripts": [
            "realbbc=bbc.__main__:main",
        ]
    },
)
