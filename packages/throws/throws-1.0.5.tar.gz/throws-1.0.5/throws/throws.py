#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
from typing import Any


class EmptyListException(Exception):
    """
    Exception which is thrown when no exception or error is provided to the decorator @throws(...)
    and therefor the list is empty!
    """
    pass


class InvalidRaisedException(Exception):
    """
    Exception which is thrown when decorator @throws(...) does not contain all throwable
    exceptions for decorated function!
    """
    pass


def throws(*errors: Any):
    """
    Decorator for functions equal to the "@throws(...)" decorator provided by Kotlin to specify
    possible exceptions or errors thrown!

    :param errors: list of possible exceptions
    :return: function with decorator wrapped around
    :exception EmptyListException: when no exception or error is provided in decorator
    :exception InvalidRaisedException: when an exception or error is thrown which is not provided
    """
    
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if len(errors) <= 0:
                raise EmptyListException(
                    "List of possible exceptions provided to decorator can not be empty!"
                )

            try:
                return function(*args, **kwargs)
            except Exception as err:
                for exception in errors:
                    if isinstance(err, exception):
                        raise err
                
                raise InvalidRaisedException(
                    f"Exception {err.__class__.__name__} missing in list for decorator at "
                    + f"function '{function.__name__}'!"
                ) from None
        
        return wrapper
    return decorator
