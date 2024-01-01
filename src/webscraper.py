import requests
from src.selenium_grid import get_webdriver
from bs4 import BeautifulSoup


def scrape(url):
    try:
        driver = get_webdriver()
        driver.get(url)
        page_source = driver.page_source
    except Exception as e:
        print("Failed to get page using WebDriver. Instructions for building and running a"
              " Selenium Grid Docker container can be found in the README.md file.")
        print(str(e))
        return None
    else:
        soup = BeautifulSoup(page_source, 'html.parser')
    return soup

if __name__ == "__main__":
    url = "http://example.com"
    result = scrape(url)
    print(result)
