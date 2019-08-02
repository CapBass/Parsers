import requests
import json
import re
from bs4 import BeautifulSoup


def request_avito(region='habarovsk'):
    request_str = f'https://www.avito.ru/{region}/kvartiry'
    try:
        responce = requests.get(request_str).text
    except requests.exceptions.ConnectionError:
        print('Соединение не установлено')
        exit(1)
    soup = BeautifulSoup(responce, 'html.parser')
    ads = soup.findAll('div', {'class': re.compile('js-catalog-item-enum')})
    return ads


print(request_avito()[0])
