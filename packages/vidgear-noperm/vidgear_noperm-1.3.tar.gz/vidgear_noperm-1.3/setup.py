"""

This library is forked from abhiTronix's vidgear, and modified for easy use.
Go to https://github.com/abhiTronix/vidgear/issues if you have any issues, questions, bug reports or feature requests.

"""
# import the necessary packages
import json
import sys
import platform
import setuptools
import urllib.request

from pkg_resources import parse_version
from distutils.util import convert_path
from setuptools import setup


def test_opencv():
    """
    This function is workaround to
    test if correct OpenCV Library version has already been installed
    on the machine or not. Returns True if previously not installed.
    """
    try:
        # import OpenCV Binaries
        import cv2

        # check whether OpenCV Binaries are 3.x+
        if parse_version(cv2.__version__) < parse_version("3"):
            raise ImportError(
                "Incompatible (< 3.0) OpenCV version-{} Installation found on this machine!".format(
                    parse_version(cv2.__version__)
                )
            )
    except ImportError:
        return True
    return False


def latest_version(package_name):
    """
    Get latest package version from pypi (Hack)
    """
    url = "https://pypi.python.org/pypi/%s/json" % (package_name,)
    try:
        response = urllib.request.urlopen(urllib.request.Request(url), timeout=1)
        data = json.load(response)
        versions = data["releases"].keys()
        versions = sorted(versions)
        return ">={}".format(versions[-1])
    except:
        pass
    return ""


pkg_version = {}
ver_path = convert_path("vidgear_noperm/version.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), pkg_version)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    long_description = long_description.replace(  # patch for images
      "docs/overrides/assets", "https://abhitronix.github.io/vidgear/assets"
    )
    # patch for unicodes
    long_description = long_description.replace("➶", ">>")
    long_description = long_description.replace("©", "(c)")

setup(
    name="vidgear_noperm",
    packages=["vidgear_noperm", "vidgear_noperm.gears", "vidgear_noperm.gears.asyncio"],
    version=pkg_version["__version__"],
    description="A modified variation of abhiTronix's vidgear. In this variation, it is possible to write the output file anywhere regardless the permissions.",
    license="Apache License 2.0",
    author="Ege Akman",
    install_requires=[
        "pafy{}".format(latest_version("pafy")),
        "mss{}".format(latest_version("mss")),
        "numpy",
        "youtube-dl{}".format(latest_version("youtube-dl")),
        "streamlink{}".format(latest_version("streamlink")),
        "requests{}".format(latest_version("requests")),
        "pyzmq{}".format(latest_version("pyzmq")),
        "simplejpeg".format(latest_version("simplejpeg")),
        "colorlog",
        "colorama",
        "tqdm",
        "Pillow",
        "pyscreenshot{}".format(latest_version("pyscreenshot")),
    ]
    + (["opencv-python"] if test_opencv() else [])
    + (["picamera"] if ("arm" in platform.uname()[4][:3]) else []),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="egeakmanegeakman@hotmail.com",
    url="https://github.com/egeakman/vidgear_noperm",
    extras_require={
        "asyncio": [
            "starlette{}".format(latest_version("starlette")),
            "aiofiles",
            "jinja2",
            "aiohttp",
            "uvicorn{}".format(latest_version("uvicorn")),
            "msgpack_numpy",
        ]
        + (
            ["aiortc{}".format(latest_version("aiortc"))]
            if (platform.system() != "Windows")
            else []
        )
        + (
            (
                ["uvloop{}".format(latest_version("uvloop"))]
                if sys.version_info[:2] >= (3, 7)
                else ["uvloop==0.14.0"]
            )
            if (platform.system() != "Windows")
            else []
        )
    },
    keywords=[
        "OpenCV",
        "vidgear",
        "write",
        "anywhere",
        "no",
        "permission",
        "multithreading",
        "FFmpeg",
        "picamera",
        "starlette",
        "mss",
        "pyzmq",
        "aiortc",
        "uvicorn",
        "uvloop",
        "pafy",
        "youtube-dl",
        "asyncio",
        "dash",
        "streamlink",
        "Video Processing",
        "Video Stablization",
        "Computer Vision",
        "Video Streaming",
        "raspberrypi",
        "YouTube",
        "Twitch",
        "WebRTC",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Developers",
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    scripts=[],
    project_urls={
        "Issues": "https://github.com/abhiTronix/vidgear/issues",
        "Forked From": "https://github.com/abhiTronix/vidgear",
        "Documentation": "https://abhitronix.github.io/vidgear",
        "Ege Akman's GitHub Profile": "https://github.com/egeakman",
    },
)
