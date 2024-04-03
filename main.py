from bs4 import BeautifulSoup
import requests
import lxml
import re
import time
import random
import numpy as np
from fake_useragent import UserAgent
import asyncio
import aiohttp


# https://2ip.ru

print("Введите ссылку на сайт:")
user_inp = f"{input()}"
start_time = time.time()

    # Пока будет так, возможно будет функция, которая выдает какой-то общий результат
    # Наприме, информация о всех заголовках, ссылках и т.д.
    # Либо под каждую отельную задачу будет своя функция


#Удобнее будет сделать под каждый хаголовок в таблице свою функци для сбора данных со страницы

async def get_classes(url_of_site: str) -> None:
    """Асинхронная функция, собирающая названия всех классов на сайте"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
            print("Устанавливаю соединение...")
            await asyncio.sleep(0.5)

            if response.status == 200:
                print("Соединение установлено")
                html_text = await response.text()
                html_code = BeautifulSoup(html_text, "html.parser")
                list_smth = []

                for item in html_code.findAll(class_=True):
                    classes = item['class']
                    list_smth.extend(classes)
            else:
                raise Exception("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")



async def get_hrefs(url_of_site: str) -> None:
    """Асинхронная функция, собирающая все ссылки с сайта"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
            print("Устанавливаю соединение...")
            await asyncio.sleep(0.5)

            if response.status == 200:
                print("Соединение установлено")
                html_text = await response.text()
                html_code = BeautifulSoup(html_text, "html.parser")
                list_smth = []

                for item in html_code.find_all("a", href=True):
                    href_tags = item['href']
                    list_smth.extend(href_tags)
            else:
                raise Exception("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")



async def get_headers(url_of_site: str) -> None:
    """Асинхронная функция, собирающая все заголовки с сайта"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
            print("Устанавливаю соединение...")
            await asyncio.sleep(0.5)

            if response.status == 200:
                print("Соединение установлено")
                html_text = await response.text()
                html_code = BeautifulSoup(html_text, "html.parser")
                headings = []

                for i in range(1, 7):
                    heading_tags = html_code.find_all(f"h{i}")
                    headings.extend(heading_tags)
            else:
                raise Exception("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")



async def get_divs(url_of_site: str) -> list:
    """Функиця, собирающая все блочные элементы"""
    list_smth = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
            print("Устанавливаю соединение...")
            await asyncio.sleep(0.5)
            if response.status_code == 200:
                print("Соединение установлено")
                html_text = await response.text()
                html_code = BeautifulSoup(html_text, "html.parser")
                for item in html_code.findAll("div"):
                    divs = item['div']
                    list_smth.extend(divs)
            else:
                raise Exception("Ошибка: Соединение не установлено, возможно неправильно указан URL cайта.")

    return (print(*list_smth, sep='\n'))

async def get_title(url_of_site: str) -> list:
    """Асинхронная функция, собирающая все названия"""
    list_smth = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
            print("Устанавливаю соединение...")
            await asyncio.sleep(0.5)

            if response.status == 200:
                print("Соединение установлено")
                html_text = await response.text()
                html_code = BeautifulSoup(html_text, "html.parser")

                for item in html_code.findAll("title"):
                    titles = item['title']
                    list_smth.extend(titles)
            else:
                raise Exception("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")




end_time= time.time()
program_work_time = end_time - start_time
print(f"Time:{program_work_time}"
      f"\n{end_time} - {start_time}")











# def collect_all_divs(url_of_site):
#     response = requests.get(url_of_site)
#     soup = BeautifulSoup(response.content, "html.parser")
#     divs = soup.find_all("div")
#     return divs
#
#
# def collect_all_headings(url_of_site):
#     response = requests.get(url_of_site)
#     soup = BeautifulSoup(response.content, "html.parser")
#     headings = []
#
#     for i in range(1, 7):
#         heading_tags = soup.find_all(f"h{i}")
#         headings.extend(heading_tags)
#
#     return headings
#
#
# def collect_all_href(url_of_site):
#     response = requests.get(url_of_site)
#     soup = BeautifulSoup(response.content, "html.parser")
#     href_tags = soup.find_all("a", href=True)
#
#     href_links =  [tag["href"] for tag in href_tags]
#
#     return href_links