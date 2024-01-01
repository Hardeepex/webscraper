import httpx
from selectolax.parser import HTMLParser
import time
import json

# Constants for the scraper
BASE_URL = "https://www.rei.com/c/camping-and-hiking/f/scd-deals?page={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/111.0"
}
MAX_PAGES = 100

def get_html(url):
    try:
        response = httpx.get(url, headers=HEADERS, follow_redirects=True)
        response.raise_for_status()
        return HTMLParser(response.text)
    except httpx.HTTPError as e:

# Test for 'get_html' function

import pytest
from httpx import Response
from unittest.mock import patch

def test_get_html_success():
    with patch('src.singleproduct.httpx.get') as mock_get:
        mock_get.return_value = Response(200, text="<html></html>")
        html_parser = get_html('http://example.com')
        assert type(html_parser) is HTMLParser
        assert html_parser.text() == "<html></html>"

# Execute the tests
pytest.main()
        print(f"HTTP error occurred: {e}")
        return None

def parse_page(html):
    products = html.css("li.product-tile")  # Update the selector based on the actual webpage
    for product in products:
        yield {
            "name": extract_text(product, "h3.product-title > a"),  # Update selector
            "price": extract_text(product, "div.product-price"),  # Update selector
            "savings": extract_text(product, "div.savings-class")  # Update selector
        }

def extract_text(node, selector):

# Test for 'parse_page' function

def test_parse_page():
    mock_html = HTMLParser('<ul><li class="product-tile"><h3 class="product-title"><a>Sample Product</a></h3><div class="product-price">$99.99</div><div class="savings-class">Save $20</div></li></ul>')
    result = list(parse_page(mock_html))
    assert len(result) == 1
    assert result[0]['name'] == 'Sample Product'
    assert result[0]['price'] == '$99.99'
    assert result[0]['savings'] == 'Save $20'

# Execute the tests
pytest.main()

# End of test code
    try:
        return node.css_first(selector).text()
    except AttributeError:
        return None


def main():
    for page_num in range(1, MAX_PAGES + 1):
        print(f"Gathering page {page_num}")
        full_url = BASE_URL.format(page_num)
        html = get_html(full_url)

        if html is None:
            print("Page limit exceeded or error fetching the page.")
            break

        # Debugging: Print raw HTML to inspect
    print(html.text())  # Uncomment this line to print the raw HTML

        data = parse_page(html)
        data_list = list(data)  # Convert generator to list to use it multiple times

        # Debugging: Check if any data is being extracted
        if not data_list:
            print("No data extracted from the page.")
            # Debugging: Print the HTML to inspect if selectors are wrong
            print(html.text())
        else:
            for item in data_list:
                print(item)

        time.sleep(1)  # Sleep to avoid hammering the server

if __name__ == "__main__":
    main()
