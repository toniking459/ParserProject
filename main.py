from bs4 import BeautifulSoup
import requests
import lxml
import re
import time

print("Введите ссылку на сайт:")
user_inp = f"{input()}"

def get_parse(url_of_site: str) -> list:
    """Функиця, обрабатывающая пользовательский ввод ссылки на сайт для парсинга"""

    page_to_parse = requests.get(url_of_site)
    print("Устанавливаю соединение...")
    time.sleep(0.5)
    if page_to_parse.status_code == 200:
        print("Соединение установлено")
        html_code = BeautifulSoup(page_to_parse.text, "html.parser")
        list1 = []
        for item in html_code.findAll('title'):
            list1.append(item.getText())
    else:
        raise Exception("Ошибка: Соединение не установлено")

    pass
    # Пока будет так, возможно будет функция, которая выдает какой-то общий результат
    # Наприме, информация о всех заголовках, ссылках и т.д.
    # Либо под каждую отельную задачу будет своя функция

