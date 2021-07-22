from contextlib import contextmanager
from typing import Iterator

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class CustomHTTPAdapter(HTTPAdapter):
    def __init__(self, max_retries: Retry, timeout: int, stream: bool):
        super(CustomHTTPAdapter, self).__init__(max_retries=max_retries)
        self.timeout = timeout
        self.stream = stream

    def send(self, *args, **kwargs):
        kwargs["timeout"] = self.timeout
        kwargs["stream"] = self.stream
        return super(CustomHTTPAdapter, self).send(*args, **kwargs)


@contextmanager
def requests_session(retries=3, backoff_factor=0.1, timeout=35, stream=False, **kwargs) -> Iterator[Session]:
    session = Session()

    max_retries = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        **kwargs,
    )
    adapter = CustomHTTPAdapter(max_retries, timeout, stream)

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        yield session
    finally:
        session.close()
