import ollama

def ask_ollama(product_json):
    prompt = f"Анализируй этот товар:\n{product_json}\n\nОтветь кратко (3-5 строк)"

    try:
        response = ollama.chat(
            model='llama3.2:3b',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except:
        return "Запустите Ollama: ollama serve"
