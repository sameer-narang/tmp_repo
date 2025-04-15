from enum import Enum
from numbers import Number
from typing import Any

import pytest


class Stack(Enum):
    """ represents the stacks that packages need to be put into """
    STANDARD: str = "STANDARD"
    SPECIAL: str = "SPECIAL"
    REJECTED: str = "REJECTED"


def sort(width: float, height: float, length: float, mass: float) -> str:
    """ returns the correct stack that the provided package should go to """
    
    if any(not isinstance(x, Number) for x in (width, height, length, mass)):
        raise TypeError(f"sort() called with non-numeric arguments. args: {locals()}")
    
    if any(x <= 0 for x in (width, height, length, mass)):
        raise ValueError(f"sort() called with invalid numeric arguments. args: {locals()}")

    heavy: bool = mass >= 20
    bulky: bool = any(x >= 150 for x in (width, height, length)) or \
            width * height * length >= 1_000_000

    if heavy and bulky:
        return Stack.REJECTED
    elif heavy or bulky:
        return Stack.SPECIAL
    else:
        return Stack.STANDARD


def test_sort():
    """ tests valid numeric inputs """
    test_cases: list[tuple[tuple[float, float, float, float], str]] = [
            ((1, 1, 1, 10), Stack.STANDARD),
            ((1, 1, 1, 100), Stack.SPECIAL),
            ((150, 1, 1, 7), Stack.SPECIAL),
            ((150, 1, 1, 73), Stack.REJECTED),
            ((100, 100, 100, 7), Stack.SPECIAL),
            ((100, 100, 100, 59), Stack.REJECTED),
            ((1_000_000, 1, 1, 9), Stack.SPECIAL),
            ((1_000_000, 1, 1, 98), Stack.REJECTED)
            ]
    for test in test_cases:
        assert(sort(*test[0]) == test[1])
        #print(f"{test[0]} yielded {sort(*test[0])}")

def test_invalid_input_values():
    test_cases: list[tuple[Number, Number, Number, Number]] = [
            (0, 1, 1_000_000, 7),
            (1, 0, 1_000_000, 7),
            (1, 1, -1_000_000, 7),
            (5, 6, 4, -3),
            (9, 34, 93, 0),
            ]
    for test in test_cases:
        try:
            sort(*test)
        except ValueError:
            pass
        else:
            raise AssertionError(f"ValueError not raised for {test=}")

def test_invalid_input_types():
    test_cases: list[tuple[Any, Any, Any, Any]] = [
            ("", 1, 2, 3, 4),
            (1, "", 2, 3, 4),
            (1, 2, 3, ""),
            ([], 5, 8, 10),
            (9, 4, 6, {})
            ]
    for test in test_cases:
        try:
            sort(*test)
        except TypeError:
            pass
        else:
            raise AssertionError(f"ValueError not raised for {test=}")
