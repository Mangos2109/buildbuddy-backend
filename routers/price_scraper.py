import requests
from bs4 import BeautifulSoup

def scrape_amazon_product(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        price_element = soup.select_one("span.a-price-whole")

        if price_element:
            return float(price_element.text.replace(",", "").strip())
    
    return None  # If price not found
