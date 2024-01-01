import queue


class URLManager:
    def __init__(self):
        self._url_queue = queue.Queue()

    def add_url(self, url):
        self._url_queue.put(url)

    def get_next_url(self):
        if not self._url_queue.empty():
            return self._url_queue.get()
        else:
            return None
