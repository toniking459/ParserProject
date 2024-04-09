from typing import List, Any

from bs4 import BeautifulSoup, ResultSet
import requests
import lxml
import re
import time
import random
import numpy as np
from fake_useragent import UserAgent
import asyncio
import aiohttp
import queue

# https://2ip.ru

# print("Введите ссылку на сайт:")
# user_inp = f"{input()}"
start_time = time.time()


# Пока будет так, возможно будет функция, которая выдает какой-то общий результат
# Наприме, информация о всех заголовках, ссылках и т.д.
# Либо под каждую отельную задачу будет своя функция


# Удобнее будет сделать под каждый хаголовок в таблице свою функци для сбора данных со страницы

async def get_classes(url_of_site: str) -> list:
    """Асинхронная функция, собирающая названия всех классов на сайте"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
            print("Устанавливаю соединение...")
            await asyncio.sleep(0.5)

            if response.status == 200:
                print("Соединение установлено")
                html_text = await response.text(encoding='utf-8')
                html_code = BeautifulSoup(html_text, "html.parser")
                list_smth = []

                for item in html_code.findAll(class_=True):
                    classes = item['class']
                    list_smth.extend(classes)
            else:
                raise TypeError("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")

    return list_smth


async def get_hrefs(url_of_site: str) -> list:
    """Асинхронная функция, собирающая все ссылки с сайта"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
            print("Устанавливаю соединение...")
            await asyncio.sleep(0.5)

            if response.status == 200:
                print("Соединение установлено")
                html_text = await response.text(encoding='utf-8')
                html_code = BeautifulSoup(html_text, "html.parser")
                list_smth = []

                href_tags = html_code.find_all("a", href=True)
                href_tags = [tag["href"] for tag in href_tags]
                list_smth.extend(href_tags)
            else:
                raise TypeError("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")
    return list_smth


async def get_headers(url_of_site: str) -> str:
    """Асинхронная функция, собирающая все заголовки с сайта."""

    async with aiohttp.ClientSession() as session:
        async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
            print("Устанавливаю соединение...")
            await asyncio.sleep(0.5)

            if response.status == 200:
                print("Соединение установлено")
                html_text = await response.text(encoding='utf-8')
                html_code = BeautifulSoup(html_text, "html.parser")
                soup = BeautifulSoup(html_text, 'lxml')
                heading_list=[]
                for i in range(1,7):
                    headings = html_code.find_all(f'h{i}')
                    heading_list.extend(headings)

            else:
                raise TypeError("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")
    return f"Headings: {heading_list}\n h1: {soup.h1.text}, \t h2: {soup.h2.text}, \t h3: {soup.h3.text}, \t h4: {soup.h4.text}, \t h5: {soup.h5} , \t h6: {soup.h6.text}"


# async def get_divs(url_of_site: str) -> list:
#     """Функиця, собирающая все блочные элементы"""
#     list_smth = []
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
#             print("Устанавливаю соединение...")
#             await asyncio.sleep(0.5)
#             if response.status == 200:
#                 print("Соединение установлено")
#                 html_text = await response.text(encoding='utf-8')
#                 html_code = BeautifulSoup(html_text, "html.parser")
#                 divs =  html_code.findAll("div")
#                 list_smth.extend(divs)
#
#             else:
#                 raise Exception("Ошибка: Соединение не установлено, возможно неправильно указан URL cайта.")
#
#     return list_smth


async def get_title(url_of_site: str) -> list:
    """Асинхронная функция, собирающая все названия"""
    list_smth = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
            print("Устанавливаю соединение...")
            await asyncio.sleep(0.5)

            if response.status == 200:
                print("Соединение установлено")
                html_text = await response.text(encoding='utf-8')
                html_code = BeautifulSoup(html_text, "html.parser")

                for item in html_code.findAll("title"):
                    titles = item
                    list_smth.extend(titles)
            else:
                raise TypeError("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")
    return list_smth

predict_classes1 = (
    'container',
    'logo-wrapper',
    'logo'

)
async def get_custom_classes(url_of_site: str, predict_classes: tuple) -> list[ResultSet[Any]]:
    """Асинхронная функция, собирающая названия всех классов на сайте и ищущая определённые классы"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
            print("Устанавливаю соединение...")
            await asyncio.sleep(0.5)

            if response.status == 200:
                print("Соединение установлено")
                html_text = await response.text(encoding='utf-8')
                html_code = BeautifulSoup(html_text, "html.parser")
                list_smth = []

                for item in html_code.findAll(class_=True):
                    classes = item['class']
                    list_smth.extend(classes)

                for predict_class in predict_classes:
                    for i in range(len(list_smth)):
                        if list_smth[i].find(predict_class) != -1:
                            elements = html_code.findAll(class_=f'{list_smth[i]}')
                            list_smth.append(elements)

            else:
                raise TypeError("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")

    return list_smth


#asyncio.run(get_title("https://qna.habr.com"))

# async def main():
#     # Create the queue of 'work'
#     work_queue = asyncio.Queue()
#
#     # Put some 'work' in the queue
#     for url in [
#         "http://google.com",
#         "http://yahoo.com",
#         "http://linkedin.com",
#         "http://apple.com",
#         "http://microsoft.com",
#         "http://facebook.com",
#         "http://twitter.com"
#     ]:
#         await work_queue.put(url)
#
#     await asyncio.gather(
#         asyncio.create_task(get_hrefs(url)),
#         asyncio.create_task(get_title(url)),
#         asyncio.create_task(get_classes(url)),
#         asyncio.create_task(get_headers(url)))
#
#
# async def tasks():
#    await main()
#
#
# if __name__ == "__main__":
#    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#    asyncio.run(main())

end_time = time.time()
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
# def get_titlesd(url_of_site: str) -> list:
#     """Функиця, собирающая все названия """
#     list_smth = []
#     page_to_parse = requests.get(url_of_site, headers={'UserAgent': UserAgent().chrome})
#     print("Устанавливаю соединение...")
#     time.sleep(0.5)
#     if page_to_parse.status_code == 200:
#         print("Соединение установлено")
#         html_code = BeautifulSoup(page_to_parse.text, "html.parser")
#
#         for item in html_code.findAll("title"):
#             titles = item.text
#             list_smth.extend(titles)
#
#     else:
#         raise Exception("Ошибка: Соединение не установлено, возможно неправильно указан URL cайта.")
#
#     return list_smth

print(asyncio.run(get_classes("https://qna.habr.com")))
print(asyncio.run(get_title("https://qna.habr.com")))
print(asyncio.run(get_hrefs("https://qna.habr.com")))
print(asyncio.run(get_headers("https://qna.habr.com")))
# print(asyncio.run(get_custom_classes("https://qna.habr.com",predict_classes1)))