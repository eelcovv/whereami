import os
from pathlib import Path
import logging

_logger = logging.getLogger(__name__)
try:
    from latloncalc import latlon as llc
except ModuleNotFoundError as err:
    _logger.warning("{err}")
    llc = None

try:
    import country_converter as coco
except ModuleNotFoundError:
    _logger.warning("{err}")
    coco = None


def deg_to_dms(degrees_decimal: float, n_digits_seconds: int = 1):
    """
    Turn a number in decimal to a sexagesimal representation degrees-minutes-seconds

    Args:
        degrees_decimal: float
            Degrees in decimal representation

        n_digits_seconds:
            Number of digits to use for the seconds of the sexagesimal respresentation

    Returns: str
        Sexagesimal representation of the location in degrees-minutes-seconds
    """
    degrees = int(degrees_decimal)
    minutes_decimal = abs(degrees_decimal - degrees) * 60
    minutes = int(minutes_decimal)
    seconds_decimal = round((minutes_decimal - minutes) * 60, n_digits_seconds)
    dms_coordinates = f"{degrees}° {minutes}' {seconds_decimal}″"
    return dms_coordinates


def make_sexagesimal_location(latitude: float, longitude: float, n_digits_seconds: int = 1):
    """
    Turns the latitude/longitude location into a sexagesimal string

    Args:
        latitude: float
            The latitude in decimal notation
        longitude: float
            The longitude in decimal notation
        n_digits_seconds: int
            Number of digits to use for the seconds of the sexagesimal representation

    Returns: str
        location as a sexagesimal string
    """
    if llc is None:
        lat_dms = deg_to_dms(latitude, n_digits_seconds=n_digits_seconds)
        lon_dms = deg_to_dms(longitude, n_digits_seconds=n_digits_seconds)
        location = f"{lat_dms}, {lon_dms}"
    else:
        latlon = llc.LatLon(lat=latitude, lon=longitude)
        location = latlon.to_string(formatter="d%° %m%′ %S%″ %H", n_digits_seconds=n_digits_seconds)

    return location


def make_decimal_location(latitude: float, longitude: float, n_decimals: int = 1):
    """
    Turns the latitude/longitude location into a decimal string

    Args:
        latitude: float
            The latitude in decimal notation
        longitude: float
            The longitude in decimal notation
        n_decimals: int
            Number of digits to use for the decimal representation

    Returns: str
        location as a decimal string
    """
    strfrm = "{:." + f"{n_decimals}" + "f}"
    location = ", ".join([strfrm.format(latitude), strfrm.format(longitude)])
    return location


def make_human_location(country_code: str, city: str):
    """
    Turns the country and city strings into a country/city representation

    Args:
        country_code: str
            The country code of the location
        city: str
            The city of the location

    Returns: str
        Either city / country (country_code)  or city /country_code
    """
    if coco is not None:
        country_name = coco.convert(country_code, to="name_short")
        country = country_name + f" ({country_code})"
    else:
        country = country_code
    location = f"{city}/{country}"
    return location


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
