import pytest

from whereami.getgeolocation import (main)

__author__ = "eelco"
__copyright__ = "eelco"
__license__ = "MIT"


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["--no_write_cache",
          "--ip_address", "8.8.8.8",
          "--my_location", "Amsterdam,The Netherlands"])
    captured = capsys.readouterr()
    expected = "Server 8.8.8.8 @ Mountain View/United States (US) has coordinates (37° 24′ 20.2″ N, 122° 4′ 39.0″ W)\n" \
               "Distance from Amsterdam,The Netherlands (52° 22′ 21.9″ N, 4° 53′ 37.0″ E):  8816km.\n"
    assert expected in captured.out
