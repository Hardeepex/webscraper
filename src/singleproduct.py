import httpx
from selectolax.parser import HTMLParser

def extract_text(node, selector):
    try:
        return node.css_first(selector).text()
    except AttributeError:
        return None

url = "https://www.rei.com/c/camping-and-hiking/f/scd-deals"
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
