import os

def write_to_html(header, contents, filename="output.html"):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>{header}</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                margin: 40px;
                background: #f5f5f5;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }}
            h1 {{ 
                color: #333;
                border-bottom: 2px solid #4a6fa5;
                padding-bottom: 10px;
            }}
            .text-block {{
                background: #f8f9fa;
                border-left: 4px solid #4a6fa5;
                padding: 20px;
                margin-top: 20px;
                border-radius: 5px;
                line-height: 1.6;
                white-space: pre-line;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{header}</h1>
            <div class="text-block">{contents.replace(chr(10), '<br>')}</div>
        </div>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML-файл сохранён как {os.path.abspath(filename)}")

def write_to_txt(header, contents, filename="output.txt"):
    txt_content = f"{header}\n{'='*len(header)}\n\n{contents}"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(txt_content)
    print(f"Текстовый файл сохранён как {os.path.abspath(filename)}")


