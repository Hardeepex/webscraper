import time


class RateLimiter:
    def __init__(self):
        self._last_request_time = time.time()

    def wait(self):
        time_since_last_request = time.time() - self._last_request_time
        if time_since_last_request < 1:
            time.sleep(1 - time_since_last_request)
        self._last_request_time = time.time()

# Test suite for RateLimiter
import unittest
class TestRateLimiter(unittest.TestCase):
    def test_wait(self):
        rate_limiter = RateLimiter()
        start_time = time.time()
        for _ in range(4):
            rate_limiter.wait()
        self.assertGreaterEqual(time.time() - start_time, 3, "The RateLimiter class should enforce at least 1 second between requests.")
