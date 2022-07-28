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

from whereami import __version__

__author__ = "eelco"
__copyright__ = "eelco"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


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
    except IndexError:
        _logger.debug(f"Answer was {answer}")
    else:
        if first_char == "y":
            positive = True
        elif first_char == "n":
            positive = False
        else:
            _logger.warning("Please answer with [y/N] only.")
            positive = query_yes_no(message)

    return positive


def get_config_file() -> Path:
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
    config_file = config_dir / Path("whereami.conf")

    return config_file


def get_api_key() -> str:
    """
    Get the current api key

    Returns: str
        Current api key
    """
    config_file = get_config_file()

    with open(config_file, "r") as stream:
        settings = yaml.load(stream, Loader=yaml.FullLoader)
        current_api_key = settings.get("api_key")

    if current_api_key is None:
        message = f"No api key found in {config_file}. Please specify first"
        raise EnvironmentError(message)

    return current_api_key


def set_api_key(api_key):
    config_file = get_config_file()
    if config_file.exists():
        with open(config_file, "r") as stream:
            settings = yaml.load(stream, Loader=yaml.FullLoader)
            current_api_key = settings.get("api_key")

        if current_api_key is not None:
            if current_api_key != api_key:
                if not query_yes_no(
                        f"The current api key {current_api_key} differs from {api_key}"):
                    _logger.info("Goodbye...")
                    sys.exit(0)
            else:
                _logger.info("Api key was already set before. Skip this")
                return
    else:
        settings = dict()

    settings["api_key"] = api_key

    _logger.info(f"Writing {config_file}")
    with open(config_file, "w") as stream:
        yaml.dump(settings, stream)


def getlocation():
    """Get the location
    """
    return None


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
        "--set-api-key", help="Set the API key in de config file. Request the api key at"
                              "https://ipbase.com/"
    )
    parser.add_argument(
        "--reset-cache",
        action="store_true"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="whereami {ver}".format(ver=__version__),
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

    if args.set_api_key is not None:
        set_api_key(args.set_api_key)
        sys.exit(0)

    api_key = get_api_key()
    _logger.debug(f"Retrieved api key {api_key}")

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
