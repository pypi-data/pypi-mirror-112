"""

This library is forked from abhiTronix's vidgear, and modified for easy use.
Go to https://github.com/abhiTronix/vidgear/issues if you have any issues, questions, bug reports or feature requests.

"""

# Contains all the support functions/modules required by Vidgear Asyncio packages

# import the necessary packages

import os
import cv2
import sys
import errno
import numpy as np
import aiohttp
import asyncio
import logging as log
import platform
import requests
from tqdm import tqdm
from colorlog import ColoredFormatter
from pkg_resources import parse_version
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def logger_handler():
    """
    ### logger_handler

    Returns the logger handler

    **Returns:** A logger handler
    """
    # logging formatter
    formatter = ColoredFormatter(
        "%(bold_cyan)s%(asctime)s :: %(bold_blue)s%(name)s%(reset)s :: %(log_color)s%(levelname)s%(reset)s :: %(message)s",
        datefmt="%H:%M:%S",
        reset=False,
        log_colors={
            "INFO": "bold_green",
            "DEBUG": "bold_yellow",
            "WARNING": "bold_purple",
            "ERROR": "bold_red",
            "CRITICAL": "bold_red,bg_white",
        },
    )
    # check if VIDGEAR_LOGFILE defined
    file_mode = os.environ.get("VIDGEAR_LOGFILE", False)
    # define handler
    handler = log.StreamHandler()
    if file_mode and isinstance(file_mode, str):
        file_path = os.path.abspath(file_mode)
        if (os.name == "nt" or os.access in os.supports_effective_ids) and os.access(
            os.path.dirname(file_path), os.W_OK
        ):
            file_path = (
                os.path.join(file_path, "vidgear.log")
                if os.path.isdir(file_path)
                else file_path
            )
            handler = log.FileHandler(file_path, mode="a")
            formatter = log.Formatter(
                "%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s",
                datefmt="%H:%M:%S",
            )

    handler.setFormatter(formatter)
    return handler


# define logger
logger = log.getLogger("Helper Asyncio")
logger.propagate = False
logger.addHandler(logger_handler())
logger.setLevel(log.DEBUG)


# set default timer for download requests
DEFAULT_TIMEOUT = 3


class TimeoutHTTPAdapter(HTTPAdapter):
    """
    A custom Transport Adapter with default timeouts
    """

    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def mkdir_safe(dir, logging=False):
    """
    ### mkdir_safe

    Safely creates directory at given path.

    Parameters:
        logging (bool): enables logging for its operations

    """
    try:
        os.makedirs(dir)
        if logging:
            logger.debug("Created directory at `{}`".format(dir))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        if logging:
            logger.debug("Directory already exists at `{}`".format(dir))


def create_blank_frame(frame=None, text="", logging=False):
    """
    ### create_blank_frame

    Create blank frames of given frame size with text

    Parameters:
        frame (numpy.ndarray): inputs numpy array(frame).
        text (str): Text to be written on frame.
    **Returns:**  A reduced numpy ndarray array.
    """
    # check if frame is valid
    if frame is None:
        raise ValueError("[Helper:ERROR] :: Input frame cannot be NoneType!")
    # grab the frame size
    (height, width) = frame.shape[:2]
    # create blank frame
    blank_frame = np.zeros((height, width, 3), np.uint8)
    # setup text
    if text and isinstance(text, str):
        if logging:
            logger.debug("Adding text: {}".format(text))
        # setup font
        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        # get boundary of this text
        fontScale = min(height, width) / (25 / 0.25)
        textsize = cv2.getTextSize(text, font, fontScale, 5)[0]
        # get coords based on boundary
        textX = (width - textsize[0]) // 2
        textY = (height + textsize[1]) // 2
        # put text
        cv2.putText(
            blank_frame, text, (textX, textY), font, fontScale, (125, 125, 125), 6
        )
    # return frame
    return blank_frame


async def reducer(frame=None, percentage=0):
    """
    ### reducer

    Asynchronous method that reduces frame size by given percentage.

    Parameters:
        frame (numpy.ndarray): inputs numpy array(frame).
        percentage (int/float): inputs size-reduction percentage.

    **Returns:**  A reduced numpy ndarray array.
    """
    # check if frame is valid
    if frame is None:
        raise ValueError("[Helper:ERROR] :: Input frame cannot be NoneType!")

    # check if valid reduction percentage is given
    if not (percentage > 0 and percentage < 90):
        raise ValueError(
            "[Helper:ERROR] :: Given frame-size reduction percentage is invalid, Kindly refer docs."
        )

    # grab the frame size
    (height, width) = frame.shape[:2]

    # calculate the ratio of the width from percentage
    reduction = ((100 - percentage) / 100) * width
    ratio = reduction / float(width)
    # construct the dimensions
    dimensions = (int(reduction), int(height * ratio))

    # return the resized frame
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_LANCZOS4)


def generate_webdata(path, c_name="webgear", overwrite_default=False, logging=False):
    """
    ### generate_webdata

    Auto-Generates, and Auto-validates default data for WebGear API.

    Parameters:
        path (string): path for generating data
        c_name (string): class name that is generating files
        overwrite_default (boolean): overwrite existing data or not?
        logging (bool): enables logging for its operations

    **Returns:** A valid data path as string.
    """
    # check if path corresponds to vidgear only
    if os.path.basename(path) != ".vidgear":
        path = os.path.join(path, ".vidgear")

    # generate parent directory
    path = os.path.join(path, c_name)
    mkdir_safe(path, logging=logging)

    # self-generate dirs
    template_dir = os.path.join(path, "templates")  # generates HTML templates dir
    static_dir = os.path.join(path, "static")  # generates static dir
    # generate js & css static and favicon img subdirs
    js_static_dir = os.path.join(static_dir, "js")
    css_static_dir = os.path.join(static_dir, "css")
    favicon_dir = os.path.join(static_dir, "img")

    mkdir_safe(static_dir, logging=logging)
    mkdir_safe(template_dir, logging=logging)
    mkdir_safe(js_static_dir, logging=logging)
    mkdir_safe(css_static_dir, logging=logging)
    mkdir_safe(favicon_dir, logging=logging)

    # check if overwriting is enabled
    if overwrite_default or not validate_webdata(
        template_dir, ["index.html", "404.html", "500.html"]
    ):
        logger.critical(
            "Overwriting existing WebGear data-files with default data-files from the server!"
            if overwrite_default
            else "Failed to detect critical WebGear data-files: index.html, 404.html & 500.html!"
        )
        # download default files
        if logging:
            logger.info("Downloading default data-files from the GitHub Server.")
        download_webdata(
            template_dir,
            c_name=c_name,
            files=["index.html", "404.html", "500.html", "base.html"],
            logging=logging,
        )
        download_webdata(
            css_static_dir, c_name=c_name, files=["custom.css"], logging=logging
        )
        download_webdata(
            js_static_dir,
            c_name=c_name,
            files=["custom.js"],
            logging=logging,
        )
        download_webdata(
            favicon_dir, c_name=c_name, files=["favicon-32x32.png"], logging=logging
        )
    else:
        # validate important data-files
        if logging:
            logger.debug("Found valid WebGear data-files successfully.")

    return path


def download_webdata(path, c_name="webgear", files=[], logging=False):
    """
    ### download_webdata

    Downloads given list of files for WebGear API(if not available) from GitHub Server,
    and also Validates them.

    Parameters:
        path (string): path for downloading data
        c_name (string): class name that is generating files
        files (list): list of files to be downloaded
        logging (bool): enables logging for its operations

    **Returns:** A valid path as string.
    """
    basename = os.path.basename(path)
    if logging:
        logger.debug("Downloading {} data-files at `{}`".format(basename, path))

    # create session
    with requests.Session() as http:
        for file in files:
            # get filename
            file_name = os.path.join(path, file)
            # get URL
            file_url = "https://raw.githubusercontent.com/abhiTronix/vidgear-vitals/master/{}{}/{}/{}".format(
                c_name, "/static" if basename != "templates" else "", basename, file
            )
            # download and write file to the given path
            if logging:
                logger.debug("Downloading {} data-file: {}.".format(basename, file))

            with open(file_name, "wb") as f:
                # setup retry strategy
                retries = Retry(
                    total=3,
                    backoff_factor=1,
                    status_forcelist=[429, 500, 502, 503, 504],
                )
                # Mount it for https usage
                adapter = TimeoutHTTPAdapter(timeout=2.0, max_retries=retries)
                http.mount("https://", adapter)
                response = http.get(file_url, stream=True)
                response.raise_for_status()
                total_length = response.headers.get("content-length")
                assert not (
                    total_length is None
                ), "[Helper:ERROR] :: Failed to retrieve files, check your Internet connectivity!"
                bar = tqdm(total=int(total_length), unit="B", unit_scale=True)
                for data in response.iter_content(chunk_size=256):
                    f.write(data)
                    if len(data) > 0:
                        bar.update(len(data))
                bar.close()
    if logging:
        logger.debug("Verifying downloaded data:")
    if validate_webdata(path, files=files, logging=logging):
        if logging:
            logger.info("Successful!")
        return path
    else:
        raise RuntimeError(
            "[Helper:ERROR] :: Failed to download required {} data-files at: {}, Check your Internet connectivity!".format(
                basename, path
            )
        )


def validate_webdata(path, files=[], logging=False):
    """
    ### validate_auth_keys

    Validates, and also maintains downloaded list of files.

    Parameters:
        path (string): path of downloaded files
        files (list): list of files to be validated
        logging (bool): enables logging for its operations

    **Returns:** A  boolean value, confirming whether tests passed, or not?.
    """
    # check if valid path or directory empty
    if not (os.path.exists(path)) or not (os.listdir(path)):
        return False

    files_buffer = []
    # loop over files
    for file in os.listdir(path):
        if file in files:
            files_buffer.append(file)  # store them

    # return results
    if len(files_buffer) < len(files):
        if logging:
            logger.warning(
                "`{}` file(s) missing from data-files!".format(
                    " ,".join(list(set(files_buffer) ^ set(files)))
                )
            )
        return False
    else:
        return True
