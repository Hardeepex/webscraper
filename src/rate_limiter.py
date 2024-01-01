import time


class RateLimiter:
    def __init__(self):
        self._last_request_time = time.time()

    def wait(self):
        time_since_last_request = time.time() - self._last_request_time
        if time_since_last_request < 1:
            time.sleep(1 - time_since_last_request)
        self._last_request_time = time.time()
