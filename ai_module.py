import ollama


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
