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
from urllib.parse import urljoin

srch_rqst = input("Введите запрос: ")
def search_without_browser(query) -> list:
    """
  Функция, которая выполняет поисковой запрос в Google

  Args:
    query: Текстовый запрос.

  Returns:
    Список URL-адресов результатов поиска.
  """
    # URL поискового запроса Google
    url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('a')
    base_url = "https://www.google.com/"
    links = [urljoin(base_url, result['href']) for result in results]

    return links

search_results = search_without_browser(srch_rqst)






start_time = time.time()



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
                heading_list = []
                for i in range(1, 7):
                    headings = html_code.find_all(f'h{i}')
                    heading_list.extend(headings)

            else:
                raise TypeError("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")
    return f"Headings: {heading_list}\n h1: {soup.h1.text}, \t h2: {soup.h2.text}, \t h3: {soup.h3.text}, \t h4: {soup.h4.text}, \t h5: {soup.h5} , \t h6: {soup.h6.text}"


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


async def get_custom_classes(url_of_site: str, predict_classes: tuple) -> list:
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

                result = []

                for predict_class in predict_classes:
                    for i in range(len(list_smth)):
                        if list_smth[i] in predict_class:
                            elements = html_code.find('div', {"class": f'{list_smth[i]}'})
                            result.append(elements)

                return result
            else:
                raise TypeError("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")


# asyncio.run(get_title("https://qna.habr.com"))

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

# print(asyncio.run(get_classes("https://qna.habr.com")))
# print(asyncio.run(get_title("https://qna.habr.com")))
# print(asyncio.run(get_hrefs("https://qna.habr.com")))
# print(asyncio.run(get_headers("https://qna.habr.com")))
# print(asyncio.run(get_custom_classes("https://qna.habr.com",predict_classes1)))


def get_html_to_llm():
    pass


end_time = time.time()
program_work_time = end_time - start_time
print(f"Time:{program_work_time}"
      f"\n{end_time} - {start_time}")
