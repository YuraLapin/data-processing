import requests
import json
from bs4 import BeautifulSoup

def fetch_page(url):
    session = requests.Session()
    response = session.get(url, timeout=10)
    response.raise_for_status()
    
    if len(response.text) > 10000: 
        return response.text
    else:
        print("Получена слишком короткая страница, возможно блокировка")
        return None



url = "https://www.citilink.ru/product/smartfon-huawei-nova-13-blk-lx9-512gb-12gb-dymchatyi-zelenyi-3g-4g-6-6-2077531/"
html_content = fetch_page(url)