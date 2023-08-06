"""Prod-ready HTTP client with timeout and retries by default."""
import importlib.metadata

import orjson
import requests.models

# pylint: disable=redefined-builtin
from requests.exceptions import ConnectionError, HTTPError, RequestException

from . import errors
from .client import HttpClient, dump_useragent, load_useragent
from .config import AnyAuth, HttpConfig
from .errors import ClientError, ServerError

__version__ = importlib.metadata.version(__name__)
__all__ = [
    "AnyAuth",
    "HttpClient",
    "HttpConfig",
    "dump_useragent",
    "load_useragent",
    "errors",
    "ConnectionError",
    "ClientError",
    "ServerError",
]

# patch for performance - use orjson for loading and dumping
requests.models.complexjson = orjson  # type: ignore

# patch the exceptions for more useful default error messages
RequestException.__getattr__ = errors.request_exception_getattr  # type: ignore
RequestException.__str__ = errors.request_exception_str  # type: ignore
ConnectionError.__str__ = errors.connection_error_str  # type: ignore
HTTPError.__str__ = errors.http_error_str  # type: ignore
