import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="random-spammer",
    version="1.0.1",
    description="Collection of functions that can be used in spamming",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sadiqush/random_spammer",
    author="Sadiqush",
    author_email="sadiqush@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["random_spammer"],
    include_package_data=True,
    install_requires=["exrex"],
    entry_points={
        "console_scripts": [
            "random_spammer=random_spammer.__init__:main",
        ]
    },
)

