# This file is placed in the Public Domain.

from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="botd",
    version="45",
    url="https://github.com/bthate/botd",
    author="Bart Thate",
    author_email="bthate@dds.nl",
    description="24/7 channel daemon",
    long_description=read(),
    license="Public Domain",
    zip_safe=True,
    include_package_data=True,
    py_modules=["ob"],
    packages=["bot"],
    data_files=[
        (
            "share/botd/",
            [
                "files/bot.1.md",
                "files/botctl.8.md",
                "files/botd.8.md",
                "files/botd.service",
                "files/botd",
            ],
        ),
        ("share/man/man1", ["man/bot.1.gz"]),
        ("share/man/man8", ["man/botctl.8.gz", "man/botd.8.gz"]),
    ],
    scripts=["bin/bot", "bin/botctl", "bin/botd"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
