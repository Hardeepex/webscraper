import httpx
from selectolax.parser import HTMLParser

def extract_text(node, selector):
    try:
        element = node.css_first(selector)
        if element is None:
            return None
        return element.text()
    except AttributeError:
        return None

from unittest.mock import MagicMock

url = "https://www.rei.com/c/camping-and-hiking/f/scd-deals"  # Original URL, kept for reference in case tests are run in a suitable environment
# Test for 'extract_text' function

def test_extract_text():
    mock_node = MagicMock()
    mock_node.css_first.return_value.text.return_value = "Text Content"
    assert extract_text(mock_node, "valid_selector") == "Text Content"

    mock_node.css_first.return_value = None
    assert extract_text(mock_node, "invalid_selector") is None

    mock_node.css_first.side_effect = AttributeError
    assert extract_text(mock_node, "selector_causing_attribute_error") is None
    print("All tests passed!")

test_extract_text()
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/111.0"
}

resp = httpx.get(url, headers=headers)

if resp.status_code == 200:
    html = HTMLParser(resp.text)

    # Use the correct class for the product listing item from your HTML snippet
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")

    for product in products:
        item = {
            "name": extract_text(product, "span[data-ui='product-title']"),  # Correct selector for product name
            "price": extract_text(product, "span[data-ui='sale-price']"),    # Correct selector for product price
        }
        print(item)
else:
    print(f"Failed to retrieve the page, status code: {resp.status_code}")
