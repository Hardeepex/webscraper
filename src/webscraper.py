import requests
from bs4 import BeautifulSoup


def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

if __name__ == "__main__":
    url = "http://example.com"
    result = scrape(url)
    print(result)
