import pytest

from whereami.utils import (deg_to_dms, get_distance_to_server, get_cache_file,
                            make_human_location, make_decimal_location, make_sexagesimal_location)

__author__ = "eelco"
__copyright__ = "eelco"
__license__ = "MIT"


def test_fib():
    """API Tests"""
    assert deg_to_dms(36) == "36° 0' 0″"
    assert deg_to_dms(4.5) == "4° 30' 0″"
