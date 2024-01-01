import httpx
from selectolax.parser import HTMLParser
from src.selenium_grid import get_webdriver
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
        driver = get_webdriver()
        driver.get(url)
        response.raise_for_status()
        html_source = HTMLParser(driver.page_source)
        driver.quit()
        return html_source
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return None

def parse_page(html):
    products = html.css("li.product-class")  # Update the selector based on the actual webpage
    for product in products:
        yield {
            "name": extract_text(product, "span.product-title-class"),  # Update selector
            "price": extract_text(product, "span.price-class"),  # Update selector
            "savings": extract_text(product, "div.savings-class")  # Update selector
        }

def extract_text(node, selector):
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
