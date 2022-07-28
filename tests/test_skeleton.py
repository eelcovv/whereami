import pytest

from whereami.getgeolocation import deg_to_dms

__author__ = "eelco"
__copyright__ = "eelco"
__license__ = "MIT"


def test_fib():
    """API Tests"""
    assert deg_to_dms(42.0) == 1
    with pytest.raises(AssertionError):
        deg_to_dms(-10)


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["7"])
    captured = capsys.readouterr()
    assert "The 7-th Fibonacci number is 13" in captured.out
