import pathlib
from setuptools import setup
from waifu_pics import __version__


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="waifu-pics",
    version=__version__,
    description="A simple command line app to open a waifu image/gif on the browser. This is a wrapper for the [waifu.pics](https://waifu.pics/docs) API.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/diptangsu/waifu-pics",
    author="Diptangsu Goswami",
    author_email="diptangsu.97@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["waifu_pics"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "waifu=waifu_pics.__main__:show_waifu",
        ]
    },
)
