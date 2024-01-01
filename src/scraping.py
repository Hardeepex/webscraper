import httpx
from selectolax.parser import HTMLParser
import time
from multiprocessing import Process, Queue
from src.url_manager import URLManager
from src.rate_limiter import RateLimiter
from src.error_handler import ErrorHandler
from src.db_manager import DBManager
from unittest.mock import MagicMock, patch
import pytest

# Tests for get_html function

def test_get_html_success():
    """Test get_html with successful HTTP response."""
    with patch('httpx.get') as mock_get:
        mock_get.return_value = MagicMock(status_code=200, text='<html>Success</html>')
        url_manager = MagicMock()
        url_manager.get_next_url.return_value = 'http://example.com'
        rate_limiter = MagicMock()
        rate_limiter.wait = MagicMock(return_value=None)
        error_handler = MagicMock()
        html_parser = get_html(url_manager, rate_limiter, error_handler)
        assert isinstance(html_parser, HTMLParser), 'Should return an HTMLParser instance'
        assert html_parser.html == '<html>Success</html>', 'The HTML content should match the mock response'


def test_get_html_http_error():
    """Test get_html with HTTP error."""
    with patch('httpx.get') as mock_get:
        mock_get.return_value.raise_for_status.side_effect = httpx.HTTPError('HTTP Error')
        url_manager = MagicMock()
        url_manager.get_next_url.return_value = 'http://example.com'
        rate_limiter = MagicMock()
        rate_limiter.wait = MagicMock(return_value=None)
        error_handler = MagicMock()
        error_handler.handle_error = MagicMock(return_value=None)
        result = get_html(url_manager, rate_limiter, error_handler)
        assert result is None, 'Should return None on HTTP error'
        error_handler.handle_error.assert_called_once(), 'Error handler should be called'


def test_get_html_blank_response():
    """Test get_html with blank response."""
    with patch('httpx.get') as mock_get:
        mock_get.return_value = MagicMock(status_code=200, text='')
        url_manager = MagicMock()
        url_manager.get_next_url.return_value = 'http://example.com'
        rate_limiter = MagicMock()
        rate_limiter.wait = MagicMock(return_value=None)
        error_handler = MagicMock()
        result = get_html(url_manager, rate_limiter, error_handler)
        assert result is None, 'Should return None on blank response'


def test_get_html_no_url():
    """Test get_html with no URL."""
    url_manager = MagicMock()
    url_manager.get_next_url.return_value = None
    rate_limiter = MagicMock()
    error_handler = MagicMock()
    result = get_html(url_manager, rate_limiter, error_handler)
    assert result is None, 'Should return None when there is no URL to process'

# Run tests
pytest.main()

def get_html(url_manager, rate_limiter, error_handler):
    while True:
        url = url_manager.get_next_url()
        if not url:
            return None
        rate_limiter.wait()
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/111.0"
        }
        try:
            resp = httpx.get(url, headers=headers, follow_redirects=True)
            if resp.text == '':
                print(f"Blank response for {resp.url}. Moving to the next URL.")
                return None
            resp.raise_for_status()
            return HTMLParser(resp.text)
        except httpx.HTTPError as exc:
            error_handler.handle_error(exc)
        except Exception as e:
            print(f'An unexpected error occurred while fetching URL: {e}')
            print(f'An unexpected error occurred: {e}')

def extract_text(html, sel):
    try:
        return html.css_first(sel).text()
    except AttributeError:
        return None

def parse_page(html):
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")
    for product in products:
        item = {
           "name": extract_text(product, "span[data-ui='product-title']"),
            "price": extract_text(product, "span[data-ui='sale-price']"),
            "savings": extract_text(product, "span[data-ui='savings']"),
        }
        yield item

def scrape_page(url_manager, rate_limiter, error_handler, db_manager):
    html = get_html(url_manager, rate_limiter, error_handler)
    if html is not None:
        data = parse_page(html)
        for item in data:
            db_manager.insert_data(item)

def main():
    url_manager = URLManager()
    for x in range(1, 100):
        url_manager.add_url(f"https://www.rei.com/c/camping-and-hiking/f/scd-deals?page={x}")
    rate_limiter = RateLimiter()
    error_handler = ErrorHandler(max_retries=5, retry_wait_time=1)
    db_manager = DBManager('products.db')
    db_manager.create_table()
    # Initiate multiple processes for scraping
    process_list = []
    while url_manager.get_next_url() is not None:
        process = Process(target=scrape_page, args=(url_manager, rate_limiter, error_handler, db_manager))
        process.start()
        process_list.append(process)
    # Join the processes once they are done
    for process in process_list:
        process.join()

if __name__ == "__main__":
    main()
