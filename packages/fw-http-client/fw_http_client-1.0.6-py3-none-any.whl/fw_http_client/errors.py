"""HTTP client errors."""
import io
import json
import re
import typing as t

# pylint: disable=wildcard-import,unused-wildcard-import,redefined-builtin
from requests.exceptions import *

__all__ = ["ClientError", "ServerError"]


class ClientError(HTTPError):
    """The server returned a response with 4xx status."""


class ServerError(HTTPError):
    """The server returned a response with 5xx status."""


def request_exception_getattr(self, name: str):
    """Proxy the response and the request attributes for convenience."""
    try:
        return getattr(self.response, name)
    except AttributeError:
        pass
    try:
        return getattr(self.request, name)
    except AttributeError:
        pass
    raise AttributeError(f"{type(self).__name__} has no attribute {name!r}")


def request_exception_str(self) -> str:
    """Return the string representation of a RequestException."""
    return f"{self.method} {self.url} - {self.args[0]}"  # pragma: no cover


def connection_error_str(self) -> str:
    """Return the string representation of a ConnectionError."""
    msg = str(self.args[0])
    if "Errno" in msg:
        msg = re.sub(r".*(\[[^']*).*", r"\1", msg)
    if "read timeout" in msg:
        msg = re.sub(r'.*: ([^"]*).*', r"\1", msg)
    return f"{self.method} {self.url} - {msg}"


def http_error_str(self) -> str:
    """Return the string representation of an HTTPError."""
    msg = f"{self.method} {self.url} - {self.status_code} {self.reason}"
    # capture the request headers
    if self.request.headers:
        headers = {}
        ignored = r"Accept|Connection|Content-Length"
        for header, value in self.request.headers.items():
            if header.lower() == "authorization" and " " in value:
                kind, token = value.split(" ", maxsplit=1)
                headers[header] = f"{kind} {'*' * len(token)}"
            elif "auth" in header.lower():
                headers[header] = "*" * len(value)
            elif not re.match(ignored, header, flags=re.IGNORECASE):
                headers[header] = value
        headers_str = json.dumps(headers, separators=(",", ":"), sort_keys=True)
        msg += f"\nRequest headers: {headers_str}"
    # capture the request body we sent
    if request_body := truncate(self.request.body):
        join = "\n" if "\n" in request_body else " "
        msg += f"\nRequest body:{join}{request_body}"
    # add anything the server had to say about the problem
    if response_content := truncate(self.response.content):
        join = "\n" if "\n" in response_content else " "
        msg += f"\nResponse body:{join}{response_content}"
    return msg


def truncate(data: t.Union[t.IO, bytes, str, None], max_length: int = 256) -> str:
    """Return payload truncated to the specified length as a string."""
    if not data:
        return ""
    if name := getattr(data, "name", None):  # data=open(file)
        return f"file://{name}"
    if isinstance(data, io.BytesIO):
        data = data.getvalue()
    try:
        data_str = data.decode()  # type: ignore
    except (AttributeError, UnicodeDecodeError):
        data_str = str(data)
    if len(data_str) > max_length:
        data_str = data_str[: max_length - 3].rstrip() + "..."
    return data_str
