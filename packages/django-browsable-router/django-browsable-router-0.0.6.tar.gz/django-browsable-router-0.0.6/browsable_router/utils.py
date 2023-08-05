"""API utilities."""

from typing import Union
from types import FunctionType
from itertools import chain
from functools import wraps
from contextlib import contextmanager

from django.conf import settings
from django.utils.translation import override

from rest_framework.request import Request


__all__ = ["get_language", "translate"]


available_languages = [key for (key, value) in settings.LANGUAGES]


def get_language(request: Request) -> str:
    """Get language based on request Accept-Language header or 'lang' query parameter."""
    if (lang := request.query_params.get("lang")) in available_languages:
        return lang
    elif getattr(request, "LANGUAGE_CODE", None) in available_languages:
        return request.LANGUAGE_CODE

    return "en" if "en" in available_languages else available_languages[0]


def translate(func_or_request: Union[FunctionType, Request]):
    """Override current language with one from language header or 'lang' parameter.
    Can be used as a context manager or a decorator. If a function is decorated,
    one of the parameters for the function must be a rest_framework.Request object.
    """

    @wraps(func_or_request)
    def decorator(*args, **kwargs):
        request = None
        for arg in chain(args, kwargs.values()):
            if isinstance(arg, Request):
                request = arg
                break

        if request is None:
            raise ValueError("No Request-object in function parameters.")

        with override(get_language(request)):
            return func_or_request(*args, **kwargs)

    @contextmanager
    def context_manager(request: Request):
        with override(get_language(request)):
            yield

    if isinstance(func_or_request, Request):
        return context_manager(func_or_request)
    else:
        return decorator
