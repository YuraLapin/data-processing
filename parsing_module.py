import requests
import re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print("Ошибка загрузки:", e)
        return None

def parse_basic_info(html):
    soup = BeautifulSoup(html, "html.parser")

    title = None
    price = None

    title_tag = soup.find("h1")
    if title_tag:
        title = title_tag.get_text(strip=True)

    price_tag = soup.find(attrs={"data-meta-price": True})
    if price_tag:
        price = price_tag["data-meta-price"]

    return title, price

def fetch_full_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        browser.close()
        return html

def parse_characteristics(html):
    soup = BeautifulSoup(html, "html.parser")
    characteristics = {}

    items = soup.select("div[class*='PropertiesItem']")
    for item in items:
        name_tag = item.select_one("span[class*='PropertiesItemTitle']")
        value_tag = item.select_one("span[class*='PropertiesValue']")

        if name_tag and value_tag:
            name = name_tag.get_text(strip=True)
            value = value_tag.get_text(strip=True)
            characteristics[name] = value

    return characteristics

def parse_citilink_product(url):
    html = fetch_page(url)
    if not html:
        return None

    title, price = parse_basic_info(html)

    properties_url = url.rstrip("/") + "/properties/"
    full_html = fetch_full_html(properties_url)

    characteristics = parse_characteristics(full_html)

    product = {
        "title": title,
        "price": price,
        "characteristics": characteristics,
        "source": "citilink"
    }

    return product
