__all__: tuple[str, ...] = ("HTTPError",)


class HTTPError(Exception):
    """A default exception to be raised when an error with a HTTP request occurs"""
