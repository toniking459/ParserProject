import json
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
import g4f
from g4f.client import Client
from g4f.Provider import Bing
from g4f.cookies import set_cookies



g4f_client = Client(text_provider=Bing)
g4f.debug.logging = True

proxies = {
    "all": "https://77.221.157.206:3128/",
    "https": "https://77.221.157.206:3128/"
}
client = Client(proxies=proxies)
proxy = client.get_proxy()
set_cookies(".bing.com",
            {"_U": "14MVg1d8CRJ5aTn7A-TrBe5THL5mqGJgqhC5f3DE-kY5E27oOJjz2vJ7q8n3di_XeXw-NWLvrdOs5SVbLsTqpsZcuoKC1EejslqbjQW4_kbDCkreYhS8_2fCoLkTpQbroR4WlBL3JlEnK9mJBeSpL1fPelpszSQEbV0ttR1qJrrRMO0gO81_cdge-bvcmQtDFAVwERbM24f3TPy3Rw4sPnk2Bbcj5br-oWhuFJDiMa4R74f4SmyWQJkSOEEz1-x67LTtC_QeHiDGerKhsKA95nw"}
)


srch_rqst = input("Введите запрос: ")


def search_without_browser(query) -> list:
    """
  Функция, которая выполняет поисковой запрос в Google

  Args:
    query: Текстовый запрос.

  Returns:
    Список URL-адресов результатов поиска.
  """
    url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('a')
    base_url = "https://www.google.com/"
    links = [urljoin(base_url, result['href']) for result in results]
    pattern = r"^https://www\.google\.com/url\?esrc=s&q=&rct=j&sa=U&url=https://.*$"
    links1 = []
    for result in links:
        match = re.match(pattern, result)
        corr_link = ''
        if bool(match):
            corr_link = result
            links1.append(corr_link)

    return links1
print(search_without_browser(srch_rqst))


def get_html_to_llm(usr_rqst: str, urls_from_search: list) -> list:
    """
Отправляет контент каждой страницы из списка в ChatGPT и возвращает ответы.

Args:
    usr_rqst: Пользовательский запрос.
    urls_from_search: Список URL-адресов.

Returns:
    Список ответов ChatGPT.
"""
    responses = []
    for url in urls_from_search:
        response = requests.get(url, headers={'UserAgent': UserAgent().chrome})
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text(separator=" ", strip=True)
        chat_response = g4f_client.chat.completions.create(
            provider=Bing, model="Copilot",
            messages=[{"role": "user", "content": f"Найди {usr_rqst} из страницы: {url}"}],
        )
        responses.append(chat_response.choices[0].message.content)
        print(page_text)
    return responses


# search_results = search_without_browser(srch_rqst)
# pattern = r"^https://www\.google\.com/ur\l\?esrc=s&q=&rct=j&sa=U&url=https://.*$"
# for result in search_results:
#     match = re.match(pattern, result)
#     if bool(match):
#         print(result)
#
usr_rqst = input("Введите запрос для ИИ: ")
start_time = time.time()
print(get_html_to_llm(usr_rqst, search_without_browser(srch_rqst)))

#
#
#
# async def get_classes(url_of_site: str) -> list:
#     """Асинхронная функция, собирающая названия всех классов на сайте"""
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
#             print("Устанавливаю соединение...")
#             await asyncio.sleep(0.5)
#
#             if response.status == 200:
#                 print("Соединение установлено")
#                 html_text = await response.text(encoding='utf-8')
#                 html_code = BeautifulSoup(html_text, "html.parser")
#                 list_smth = []
#
#                 for item in html_code.findAll(class_=True):
#                     classes = item['class']
#                     list_smth.extend(classes)
#             else:
#                 raise TypeError("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")
#
#     return list_smth
#
#
# async def get_hrefs(url_of_site: str) -> list:
#     """Асинхронная функция, собирающая все ссылки с сайта"""
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
#             print("Устанавливаю соединение...")
#             await asyncio.sleep(0.5)
#
#             if response.status == 200:
#                 print("Соединение установлено")
#                 html_text = await response.text(encoding='utf-8')
#                 html_code = BeautifulSoup(html_text, "html.parser")
#                 list_smth = []
#
#                 href_tags = html_code.find_all("a", href=True)
#                 href_tags = [tag["href"] for tag in href_tags]
#                 list_smth.extend(href_tags)
#             else:
#                 raise TypeError("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")
#     return list_smth
#
#
# async def get_headers(url_of_site: str) -> str:
#     """Асинхронная функция, собирающая все заголовки с сайта."""
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
#             print("Устанавливаю соединение...")
#             await asyncio.sleep(0.5)
#
#             if response.status == 200:
#                 print("Соединение установлено")
#                 html_text = await response.text(encoding='utf-8')
#                 html_code = BeautifulSoup(html_text, "html.parser")
#                 soup = BeautifulSoup(html_text, 'lxml')
#                 heading_list = []
#                 for i in range(1, 7):
#                     headings = html_code.find_all(f'h{i}')
#                     heading_list.extend(headings)
#
#             else:
#                 raise TypeError("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")
#     return f"Headings: {heading_list}\n h1: {soup.h1.text}, \t h2: {soup.h2.text}, \t h3: {soup.h3.text}, \t h4: {soup.h4.text}, \t h5: {soup.h5} , \t h6: {soup.h6.text}"
#
#
# async def get_title(url_of_site: str) -> list:
#     """Асинхронная функция, собирающая все названия"""
#     list_smth = []
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
#             print("Устанавливаю соединение...")
#             await asyncio.sleep(0.5)
#
#             if response.status == 200:
#                 print("Соединение установлено")
#                 html_text = await response.text(encoding='utf-8')
#                 html_code = BeautifulSoup(html_text, "html.parser")
#
#                 for item in html_code.findAll("title"):
#                     titles = item
#                     list_smth.extend(titles)
#             else:
#                 raise TypeError("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")
#     return list_smth
#
#
# predict_classes1 = (
#     'container',
#     'logo-wrapper',
#     'logo'
#
# )
#
#
# async def get_custom_classes(url_of_site: str, predict_classes: tuple) -> list:
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url_of_site, headers={'UserAgent': UserAgent().chrome}) as response:
#             print("Устанавливаю соединение...")
#             await asyncio.sleep(0.5)
#
#             if response.status == 200:
#                 print("Соединение установлено")
#                 html_text = await response.text(encoding='utf-8')
#                 html_code = BeautifulSoup(html_text, "html.parser")
#                 list_smth = []
#
#                 for item in html_code.findAll(class_=True):
#                     classes = item['class']
#                     list_smth.extend(classes)
#
#                 result = []
#
#                 for predict_class in predict_classes:
#                     for i in range(len(list_smth)):
#                         if list_smth[i] in predict_class:
#                             elements = html_code.find('div', {"class": f'{list_smth[i]}'})
#                             result.append(elements)
#
#                 return result
#             else:
#                 raise TypeError("Ошибка: Соединение не установлено, возможно неправильно указан URL сайта.")
#

# print(asyncio.run(get_classes("https://qna.habr.com")))
# print(asyncio.run(get_title("https://qna.habr.com")))
# print(asyncio.run(get_hrefs("https://qna.habr.com")))
# print(asyncio.run(get_headers("https://qna.habr.com")))
# print(asyncio.run(get_custom_classes("https://qna.habr.com",predict_classes1)))

end_time = time.time()
program_work_time = end_time - start_time
print(f"Time:{program_work_time}"
      f"\n{end_time} - {start_time}")
