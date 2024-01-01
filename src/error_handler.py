import time

import httpx


class ErrorHandler:
    def __init__(self, max_retries=3, retry_wait_time=1):
        self.max_retries = max_retries
        self.retry_wait_time = retry_wait_time

    def handle_error(self, error):
        if isinstance(error, httpx.HTTPStatusError):
            for _ in range(self.max_retries):
                time.sleep(self.retry_wait_time)
                try:
                    response = httpx.get(error.request.url, headers=error.request.headers)
                    response.raise_for_status()
                    return response
                except httpx.HTTPStatusError:
                    continue
        raise error
