import math
import data_bases_specialists
import requests
from bs4 import BeautifulSoup

FIO = data_bases_specialists.Specialist.get_fio(data_bases_specialists.specialist)

HOST = "http://nrs.nostroy.ru/"
URL = f'http://nrs.nostroy.ru/?s_registrationNumber=&s_fio={FIO}&s_inclusionProtocolDate=&s_suspensionProtocolDate=&s_workType=&s_statusCode=active&sort=s.id&direction=ASC&page=1'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}



def get_content(html):
    """
    Выбирает ссылки на картинки из <table> и записывает полный путь для каждой картинки
    :param html: получает страницу сайта в тексте
    :type html: str
    :return: список состоящий из словарей, каждый словарь состоит из key-порядковый номер добавления в список;
    value-список из ссылок на 3 картинки (номер, ФИО, дата)
    """
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('table', class_='table')
    cards = list()
    num_i_elem = 0
    for i_item in items:
        img = [HOST + url_img.get('src')[3:] for url_img in i_item.find_all('img')]
        for _ in range(len(img) // 3):
            cards.append((img[num_i_elem: num_i_elem + 3]))
            num_i_elem += 3
    return cards


def pages_in_pagination(html):
    """
    Находит количество листов
    :param html: получает страницу сайта в тексте
    :type html: str
    :return:
    """
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='col-md-6 count-wrapper')
    pages = [int(num) for iteam in items for i_elem in iteam.find_all('div', class_='tatal-count-wrapper')
             for num in i_elem.find('p').text.split() if num.isdigit()]

    return math.ceil(max(pages) / 20)


def parser():
    """
    Парсит страницы сайта по алгоритму, который определен в функции get_content(html) и записывает все в отдельный файл
    с помощью функции create_data_file_txt(data)
    """
    PAGES = pages_in_pagination(requests.get(URL).text)  # Количество страниц которые необходимо спарсить
    html = requests.get(URL, headers=HEADERS, params={'page': PAGES})
    if html.status_code == 200:
        cards = list()
        for page in range(1, PAGES + 1):
            print('Собираются данные со страницы: {page}'.format(page=page))
            html = requests.get(URL, headers=HEADERS, params={'page': page})
            cards.extend(get_content(html.text))
        return cards


# print(parser())