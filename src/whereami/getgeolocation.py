"""
This script get the location of the current server
"""

import argparse
import logging
import sys
import os
from pathlib import Path
import requests
import yaml
import json
import pprint

from whereami import __version__

__author__ = "eelco"
__copyright__ = "eelco"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

OUTPUT_FORMATS = {"raw", "human", "decimal", "sexagesimal"}


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from whereami.skeleton import fib`,
# when using this Python module as a library.

def query_yes_no(message):
    answer = input(f"{message}. Continue? [y/N]")
    if answer == "":
        answer = "n"
    try:
        first_char = answer.lower()[0]
    except AssertionError:
        raise AssertionError("Could not get first character. This should not happen")

    if first_char == "y":
        positive = True
    elif first_char == "n":
        positive = False
    else:
        _logger.warning("Please answer with [y/N] only.")
        positive = query_yes_no(message)

    return positive


def get_config_dir() -> Path:
    """
    Get the configuration file for this utility

    Returns:
        Path object of configuration file
    """
    try:
        home = Path(os.environ.get("HOME"))
    except TypeError:
        msg = "Cannot get home directory. Please set your HOME environment variable"
        raise TypeError(msg)

    config_dir = home / Path(".config") / Path("whereami")
    config_dir.mkdir(exist_ok=True, parents=True)
    return config_dir


def get_cache_file(ipaddress) -> Path:
    """
    Get the cache file name based on the ip address
    Args:
        ipaddress:

    Returns:

    """

    config_dir = get_config_dir()
    cache_dir = config_dir / Path("cache")
    cache_dir.mkdir(exist_ok=True)

    if ipaddress is None:
        suffix = "localhost"
    else:
        suffix = ipaddress

    cache_file = cache_dir / Path("_".join(["resp", suffix]) + ".json")
    return cache_file


def get_config_file() -> Path:
    """
    Get the configuration file for this utility

    Returns:
        Path object of configuration file
    """
    config_dir = get_config_dir()
    config_file = config_dir / Path("whereami.conf")

    return config_file


def get_response(ipaddress='8.8.8.8'):
    api_request = f"https://ipapi.co/{ipaddress}/json/"
    response = requests.get(api_request)
    if response.status_code == 200:
        _logger.info("Succesfull response")
    elif response.status_code == 407:
        _logger.warning(f"Rate limit reached as status is {response.status_code}")
        raise requests.exceptions.RequestException("Rate limit reached for api")
    else:
        _logger.warning(f"Someting else went wrong with code {response.status_code}")
        raise requests.exceptions.RequestException("Something else went wrong for api")
    return response


def get_geo_location(ipaddress='8.8.8.8', reset_cache=False):
    """
    Get the location of the local machine of the ip address if given
    """
    cache_file = get_cache_file(ipaddress=ipaddress)

    if not cache_file.exists() or reset_cache:
        response = get_response( ipaddress=ipaddress)
        geo_info = response.json()
        _logger.debug(f"Writing to cache {cache_file}")
        with open(cache_file, "w") as stream:
            json.dump(geo_info, stream, indent=True)
    else:
        _logger.debug(f"Reading geo_info from cache {cache_file}")
        with open(cache_file, "r") as stream:
            geo_info = json.load(stream)
    _logger.debug(f"Getting geolocation from {ipaddress}")

    return geo_info


def deg_to_dms(degrees_decimal):
    degrees = int(degrees_decimal)
    minutes_decimal = abs(degrees_decimal - degrees) * 60
    minutes = int(minutes_decimal)
    seconds_decimal = round((minutes_decimal - minutes) * 60, 1)
    dms_coordinates = f"{degrees}°{minutes}'{seconds_decimal}¨"
    return dms_coordinates


def create_output(geo_info, output_format=None):
    if output_format in ("decimal", "sexagesimal"):
        latitude = float(geo_info["latitude"])
        longitude = float(geo_info["longitude"])
        if output_format == "decimal":
            msg = "{lat:.2f}, {lon:.2f}".format(lat=latitude, lon=longitude)
        elif output_format == "sexagesimal":
            lat_dms = deg_to_dms(latitude)
            lon_dms = deg_to_dms(longitude)
            msg = f"{lat_dms}, {lon_dms}"
        print(msg)
    elif output_format == "human":
        country = geo_info["country_name"]
        city = geo_info["city"]
        msg = f"{city}/{country}"
        print(msg)
    elif output_format == "raw":
        pprint.pprint(geo_info)
    else:
        raise AssertionError(f"Option {output_format} not recognised")


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Get the location of your ip address")
    parser.add_argument(
        "--reset_cache",
        action="store_true"
    )
    parser.add_argument(
        "--ip_address",
        help="The ip address to get the geo location from. If not given, the local machine is used",
        default="8.8.8.8"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="whereami {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-f",
        "--format",
        help="Format of the output. Choices are: "
             "decimal: Decimal latitude/longitude (default), "
             "sexagesimal: Sexagesimal latitude/longitude,  "
             "human: Human location City/Country,"
             "raw: raw output from api",
        choices=OUTPUT_FORMATS,
        default="decimal"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--debug",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting getting location...")

    geo_info = get_geo_location(ipaddress=args.ip_address,
                                reset_cache=args.reset_cache)

    create_output(geo_info, output_format=args.format)

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m whereami.skeleton 42
    #
    run()
