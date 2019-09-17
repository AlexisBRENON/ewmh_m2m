# -*- coding: utf-8 -*-

import pytest
from ewmh_m2m.skeleton import fib

__author__ = "Alexis BRENON"
__copyright__ = "Alexis BRENON"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
