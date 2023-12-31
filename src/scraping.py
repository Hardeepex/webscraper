import httpx
from selectolax.parser import HTMLParser
import time

def get_html(baseurl, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0"
    }
    resp = httpx.get(baseurl + str(page), headers=headers, follow_redirects=True)
    try:

        resp.raise_for_status()
        return HTMLParser(resp.text)
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}. Page Limit Exceeded")
        return False

def extract_text(html, sel):
    try:
        return html.css_first(sel).text()
    except AttributeError:
        return None

def parse_page(html):
    products = html.css("li.VcGDfKky_dvNbxUqmZ9K")
    for product in products:
        item = {
           "name": extract_text(product, "span[data-ui='product-title']"),
            "price": extract_text(product, "span[data-ui=sale-price]"),
            "savings": extract_text(product, "div[data-ui=savings-percent-variant2]"),
        }
        yield item

def main():
    baseurl = "https://www.rei.com/c/camping-and-hiking/f/scd-deals?page="
    for x in range(1, 100):
        print(f"Gathering page: {x}")
        html = get_html(baseurl, x)
        if html is False:
            break
        data = parse_page(html)
        for item in data:
            print(item)
        time.sleep(1)

if __name__ == "__main__":
    main()
