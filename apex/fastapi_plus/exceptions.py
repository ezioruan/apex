import enum
from urllib.parse import urlparse

from .errors import HTTPError


class APPException(Exception):
    """
    This Exception is use to raise exception from the business logic
    """

    def __init__(self, error: enum.IntEnum):
        self.code = error.value
        self.message = error.name


class HTTPException(Exception):
    """
    This Exception is use to raise exception to the http level
    """

    def __init__(self, error: HTTPError):
        self.code = error.value
        self.message = error.name


class InternalServiceInvocationException(Exception):
    """
    The internal service invocation failed
    """

    def __init__(
        self,
        service_name: str,
        message: str,
        url: str = "",
        code=None,
        detail=None,
    ):
        self.service_name = service_name
        self.message = message
        self.code = code
        self.url = self._get_url_path(url)
        self.detail = detail

    def _get_url_path(self, url):
        if not url:
            return

        try:
            u = urlparse(url)
            return u.path
        except Exception:
            return url

    def __str__(self):
        return f"""
        [InternalServiceInvocationException#{self.service_name}]:
            ({self.code}) {self.url}
            {self.message}
            {self.detail}
        """
