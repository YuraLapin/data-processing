import json
import parsing_module
import ai_module
import pdf_export_module

url = "https://www.citilink.ru/product/televizor-led-tcl-55-55p7k-smart-chernyi-4k-ultra-hd-dvb-t-60hz-dvb-t2-2088653/"
data = parsing_module.parse_citilink_product(url)
pretty_data = json.dumps(data, ensure_ascii=False, indent=2)
print(pretty_data)

ai_answer = ai_module.ask_ollama(pretty_data)

pdf_export_module.write_to_pdf(["Анализ товара:", data["title"]], ai_answer.split("\n"))
