import requests
from bs4 import BeautifulSoup

# Test for the 'scrape' function
import pytest

def test_scrape_valid_url():
    """Test the scrape function with a valid URL."""
    test_url = 'http://example.com'
    response = scrape(test_url)
    assert response is not None
    assert 'html' in response.prettify().lower(), 'The response should contain HTML content'

# Execute the tests
pytest.main()


def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

if __name__ == "__main__":
    url = "http://example.com"
    result = scrape(url)
    print(result)
