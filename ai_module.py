import ollama
import re

def ask_ollama(product_data):
    title = product_data.get('title', '')
    price = product_data.get('price', '')

    key_characteristics = {}
    important_keys = [
        'Диагональ', 'Разрешение', 'Тип панели', 'Частота обновления',
        'Поддержка HDR', 'Операционная система', 'Яркость экрана',
        'Контрастность', 'Акустическая схема', 'Гарантия', 'Цвет'
    ]

    for key in important_keys:
        if key in product_data.get('characteristics', {}):
            key_characteristics[key] = product_data['characteristics'][key]

    prompt = f"""
    Ты эксперт по электронике. Проанализируй этот телевизор:

    Название: {title}
    Цена: {price} руб.

    Основные характеристики:
    {chr(10).join([f"• {k}: {v}" for k, v in key_characteristics.items()])}

    Вопросы для анализа:
    1. Насколько цена соответствует качеству?
    2. Какие 3 главных преимущества?
    3. Какие 2 главных недостатка?
    4. Для кого подойдет этот телевизор?
    5. Какую оценку поставишь от 1 до 10?

    ФОРМАТ ОТВЕТА (кратко):
    Оценка: X/10
    Плюсы: 1) ... 2) ... 3) ...
    Минусы: 1) ... 2) ...
    Вывод: 2-3 предложения
    """

    try:
        response = ollama.chat(
            model='llama3.2:3b',
            messages=[
                {'role': 'system', 'content': 'Ты аналитик электроники. Отвечай кратко и структурированно.'},
                {'role': 'user', 'content': prompt}
            ],
            options={
                'temperature': 0.3,
                'num_predict': 300
            }
        )
        return response['message']['content']
    except Exception as e:
        return f"Ошибка: {str(e)}. Запустите Ollama: ollama serve"

def parse_ollama_response(ai_response):
    result = {
        'rating': '',
        'pros': [],
        'cons': [],
        'summary': ''
    }

    lines = ai_response.split('\n')
    section = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if '**Оценка:**' in line:
            result['rating'] = line.replace('**Оценка:**', '').strip()
        elif '**Плюсы:**' in line or 'Плюсы:' in line:
            section = 'pros'
        elif '**Минусы:**' in line or 'Минусы:' in line:
            section = 'cons'
        elif '**Вывод:**' in line or 'Вывод:' in line:
            section = 'summary'
            if ':' in line:
                result['summary'] = line.split(':', 1)[1].strip()
        else:
            if section == 'pros' and line.startswith(('1.', '2.', '3.')):
                clean_line = re.sub(r'^\d+\.\s*', '', line)
                result['pros'].append(clean_line)
            elif section == 'cons' and line.startswith(('1.', '2.')):
                clean_line = re.sub(r'^\d+\.\s*', '', line)
                result['cons'].append(clean_line)
            elif section == 'summary' and not result['summary']:
                result['summary'] += ' ' + line
                result['summary'] = result['summary'].strip()

    return result
