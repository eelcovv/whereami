"""
This script get the location of the current server
"""

import argparse
import json
import logging
import os
import pprint
import sys
import geocoder
import socket
from pathlib import Path

import requests

from whereami import __version__
from whereami.utils import (make_sexagesimal_location,
                            make_decimal_location,
                            make_human_location,
                            get_cache_file)

__author__ = "eelco"
__copyright__ = "eelco"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

OUTPUT_FORMATS = {"raw", "human", "decimal", "sexagesimal", "full"}


class LocationReport:
    """
    Object to report the location of the server

    Args:
        geo_info: dict
            Output of geocoder
        n_digits_seconds: int
            Number of digits to use for the seconds in the d-m-s notation of the location
    """

    def __init__(self, geo_info, n_digits_seconds=1):

        self.geo_info = geo_info

        latitude = float(geo_info["lat"])
        longitude = float(geo_info["lng"])

        self.location_sexagesimal = make_sexagesimal_location(latitude=latitude,
                                                              longitude=longitude,
                                                              n_digits_seconds=n_digits_seconds)
        self.location_decimal = make_decimal_location(latitude=latitude,
                                                      longitude=longitude,
                                                      n_decimals=n_digits_seconds + 1)
        self.location_human = make_human_location(country_code=geo_info["country"],
                                                  city=geo_info["city"])

    def make_report(self, output_format: str = "sexagesimal"):
        """
        Make a report of the location

        Args:
            output_format: str
                Type of report to make:

                    decimal:        decimal representation of location
                    sexagesimal:    sexagesimal representation of location
                    human:          human representation of location
                    raw:            raw output of geolocation
                    full:           full report with all information
        """
        if output_format == "decimal":
            self.report_location_decimal()
        elif output_format == "sexagesimal":
            self.report_location_sexagesimal()
        elif output_format == "human":
            self.report_location_human()
        elif output_format == "raw":
            self.report_location_raw()
        elif output_format == "full":
            self.report_full()
        else:
            raise ValueError(f"Option {output_format} not recognised")

    def report_location_decimal(self):
        """ Print the location as a decimal representation """
        print(self.location_decimal)

    def report_location_sexagesimal(self):
        """ Print the location as a sexagesimal representation """
        print(self.location_sexagesimal)

    def report_location_human(self):
        """ Print the location as City/Country representation """
        print(self.location_human)

    def report_location_raw(self):
        """ Show the raw output of the geocoder module  """
        pprint.pprint(self.geo_info)

    def report_full(self):
        """ Give a full report of the location """
        formatter = "{:15s} : {}"
        print(formatter.format("Location (decimal)", self.location_decimal))
        print(formatter.format("Location (sexagesimal)", self.location_sexagesimal))
        print(formatter.format("Location (human)", self.location_human))


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from whereami.skeleton import fib`,
# when using this Python module as a library.


def get_response(ipaddress=None):
    if ipaddress is None:
        hostname = socket.gethostname()
        _logger.debug(f"Found local hostname {hostname}")
        local_ip = socket.gethostbyname(hostname)
        local_ip = '192.168.1.41'
        _logger.debug(f"Found local ip {local_ip}")
        api_request = 'http://freegeoip.net/json/' + local_ip
    else:
        api_request = 'http://freegeoip.net/json/' + ipaddress
    response = requests.get(api_request)
    if response.status_code != 200:
        raise requests.exceptions.RequestException("No valid response from api")
    return response


def get_geo_location_device(my_location, reset_cache=False):
    geo_info = geocoder.reverse(my_location)
    ipaddress = geo_info["ip"]

    cache_file = get_cache_file(ipaddress="my_location")

    if not cache_file.exists() or reset_cache:
        if ipaddress is None:
            geocode = geocoder.ip("me")
        else:
            geocode = geocoder.ip(ipaddress)
        geo_info = geocode.geojson['features'][0]['properties']
        with open(cache_file, "w") as stream:
            json.dump(geo_info, stream, indent=True)
    else:
        _logger.debug(f"Reading geo_info from cache {cache_file}")
        with open(cache_file, "r") as stream:
            geo_info = json.load(stream)

    return geo_info


def get_geo_location_ip(ipaddress=None, reset_cache=False):
    """
    Get the location of the local machine of the ip address if given
    """
    cache_file = get_cache_file(ipaddress=ipaddress)

    if not cache_file.exists() or reset_cache:
        if ipaddress is None:
            geocode = geocoder.ip("me")
        else:
            geocode = geocoder.ip(ipaddress)
        geo_info = geocode.geojson['features'][0]['properties']
        with open(cache_file, "w") as stream:
            json.dump(geo_info, stream, indent=True)
    else:
        _logger.debug(f"Reading geo_info from cache {cache_file}")
        with open(cache_file, "r") as stream:
            geo_info = json.load(stream)

    return geo_info


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
    parser.add_argument("--n_digits_seconds", type=int, default=1,
                        help="Number of digits to use for the seconds notation. If a decimal "
                             "notation is used, the number of decimals will be n_digit_seconds + 1")
    parser.add_argument(
        "--ip_address",
        help="The ip address to get the geo location from. If not given, the local machine is used"
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
             "full: Full report"
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
    parser.add_argument(
        "--my_location",
        help="Define the location of your device which is used to calculate the distance to "
             "the server",
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

    geo_info_ip = get_geo_location_ip(ipaddress=args.ip_address, reset_cache=args.reset_cache)

    if args.my_location is not None:
        geo_info_device = get_geo_location_device(my_location=args.my_location,
                                                  reset_cache=args.reset_cache)
        device = LocationReport(geo_info=geo_info_device,
                                n_digits_seconds=args.n_digits_seconds)
        device.make_report()

    server = LocationReport(geo_info=geo_info_ip,
                            n_digits_seconds=args.n_digits_seconds)
    server.make_report(output_format=args.format)

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
