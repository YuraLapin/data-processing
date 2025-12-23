import requests
import json
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
    with open("file.txt", "w", encoding="utf-8") as f:
        f.write(soup.prettify())
    # 1. Парсинг JSON-LD данных (самый надежный способ)
    product_data = {}
    
    # Ищем JSON-LD в скрипте
    script_tag = soup.find('script', {'type': 'application/ld+json'})
    if script_tag:
        try:
            ld_data = json.loads(script_tag.string)
            product_data['name'] = ld_data.get('name')
            product_data['sku'] = ld_data.get('sku')
            product_data['mpn'] = ld_data.get('mpn')
            product_data['brand'] = ld_data.get('brand')
            product_data['description'] = ld_data.get('description')
            product_data['rating'] = ld_data.get('aggregateRating', {}).get('ratingValue')
            product_data['review_count'] = ld_data.get('aggregateRating', {}).get('ratingCount')
            
            # Информация о предложении
            offers = ld_data.get('offers', {})
            product_data['price'] = offers.get('price')
            product_data['price_currency'] = offers.get('priceCurrency')
            product_data['availability'] = offers.get('availability')
            product_data['condition'] = offers.get('itemCondition')
            
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON-LD: {e}")
    
    # 2. Извлечение мета-информации из тегов
    meta_tags = {
        'title': soup.find('title').get_text(strip=True) if soup.find('title') else None,
        'meta_description': soup.find('meta', {'name': 'description'}).get('content', None) if soup.find('meta', {'name': 'description'}) else None,
        'canonical_url': soup.find('link', {'rel': 'canonical'}).get('href', None) if soup.find('link', {'rel': 'canonical'}) else None,
        'og_image': soup.find('meta', {'property': 'og:image'}).get('content', None) if soup.find('meta', {'property': 'og:image'}) else None,
    }
    
    # 3. Извлечение дополнительных данных из HTML-структуры
    # Артикул/код товара (часто в специальном блоке)
    code_elem = soup.find('span', {'class': lambda x: x and 'code' in x.lower()})
    if not code_elem:
        code_elem = soup.find('div', text=lambda t: t and 'Код:' in t)
    
    if code_elem:
        product_data['product_code'] = code_elem.get_text(strip=True).replace('Код:', '').strip()
    
    # 4. Хлебные крошки (breadcrumbs)
    breadcrumbs = []
    breadcrumb_elems = soup.select('a[href], span[itemprop="name"]')
    for elem in breadcrumbs:
        if elem.name == 'a' and 'href' in elem.attrs:
            breadcrumbs.append({
                'name': elem.get_text(strip=True),
                'url': elem['href']
            })
    
    # 5. Цвета/модификации (если есть)
    colors = []
    color_elems = soup.select('button[data-value], div[data-color]')
    for elem in color_elems:
        color_name = elem.get('data-value') or elem.get('data-color') or elem.get('title') or elem.get_text(strip=True)
        if color_name and color_name not in colors:
            colors.append(color_name)
    
    # 6. Характеристики товара (из блока с описанием)
    specs = []
    
    # Пробуем найти в JSON-LD описании
    if 'description' in product_data:
        desc_text = product_data['description']
        # Очищаем от HTML-тегов в описании
        if desc_text:
            desc_soup = BeautifulSoup(desc_text, 'html.parser')
            for li in desc_soup.find_all('li'):
                specs.append(li.get_text(strip=True))
    
    # Также ищем в структуре страницы
    spec_sections = soup.find_all(['div', 'section', 'table'], {'class': lambda x: x and any(word in str(x).lower() for word in ['spec', 'character', 'property', 'feature'])})
    
    for section in spec_sections:
        rows = section.find_all(['tr', 'div', 'li'])
        for row in rows:
            if row.name == 'tr':
                cols = row.find_all(['td', 'th'])
                if len(cols) >= 2:
                    spec_name = cols[0].get_text(strip=True)
                    spec_value = cols[1].get_text(strip=True)
                    if spec_name and spec_value:
                        specs.append(f"{spec_name}: {spec_value}")
            else:
                text = row.get_text(strip=True)
                if text and len(text) > 10:  # Фильтруем короткий текст
                    specs.append(text)
    
    # Удаляем дубликаты
    specs = list(dict.fromkeys(specs))
    
    # Собираем все данные
    result = {
        'product_info': product_data,
        'meta_info': meta_tags,
        'breadcrumbs': breadcrumbs[:5],  # Ограничиваем 5 элементами
        'available_colors': colors,
        'specifications': specs[:20],  # Ограничиваем 20 характеристиками
    }
    
    return result

# Тестируем
ozon_url = "https://www.citilink.ru/product/smartfon-huawei-nova-13-blk-lx9-512gb-12gb-dymchatyi-zelenyi-3g-4g-6-6-2077531/"  # Пример ссылки на товар
html_content = fetch_page(ozon_url)
data = parse_citilink_product(html_content)
print(json.dumps(data, ensure_ascii=False, indent=2))