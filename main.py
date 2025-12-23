import requests
import json
import re
from bs4 import BeautifulSoup

def fetch_page(url):
    try:
        session = requests.Session()
        response = session.get(url, timeout=10)
        response.raise_for_status()
        
        if len(response.text) > 10000:
            return response.text
        else:
            print("Получена слишком короткая страница, возможно блокировка")
            return None
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return None

def parse_citilink_product(html):
    soup = BeautifulSoup(html, 'html.parser')
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else None
    
    price_tag = soup.find(attrs={"data-meta-price": True})
    price = price_tag["data-meta-price"] if price_tag else None

    characteristics = soup.find_all('div', {'class': lambda x: x and any(
        cls.endswith('-PropertiesItem') for cls in (x if isinstance(x, list) else [x])
    )})

    
    description_tag = soup.find("div", attrs={"data-testid": "product-description"})
    description = description_tag.get_text(" ", strip=True) if description_tag else None

    rating_tag = soup.find(attrs={"data-meta-rating": True})
    rating = rating_tag["data-meta-rating"] if rating_tag else None

    code_tag = soup.find('span', {'class': lambda x: x and 'code' in x.lower()})
    code = code_tag.get_text()

    product_data = {
        "title": title,
        "price": price,
        "description": description,
        "characteristics": characteristics,
        "rating": rating,
        "source": "citilink",
        "code": code
    }

    return product_data



    

url = "https://www.citilink.ru/product/televizor-led-tcl-55-55p7k-smart-chernyi-4k-ultra-hd-dvb-t-60hz-dvb-t2-2088653/properties/" 
html_content = fetch_page(url)
data = parse_citilink_product(html_content)
print(json.dumps(data, ensure_ascii=False, indent=2))