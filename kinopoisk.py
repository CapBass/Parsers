from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import re


# from pymongo import MongoClient
# import pymongo

def parse_films(year, main_keys):
    driver = webdriver.Firefox()
    urls = get_urls_films_by_year(driver, year)
    film_data = correct_film_data(get_data_from_url(driver, urls[0], main_keys))
    print(film_data)


def get_urls_films_by_year(driver, year):
    driver.get(f'https://www.kinopoisk.ru/lists/navigator/{year}/?quick_filters=films')
    assert "КиноПоиск" in driver.title

    elements = driver.find_elements_by_class_name('selection-film-item-meta__link')
    urls = []
    for elem in elements:
        url = elem.get_attribute('href')
        urls.append(url)
    return urls


def get_data_from_url(driver, url, main_keys):
    driver.get(url)
    # time.sleep(15)
    elem = driver.find_element_by_class_name('moviename-title-wrapper')
    name = elem.text
    table = driver.find_element_by_xpath('//div[@class="movie-info__content"]//table')
    info = [item.text for item in table.find_elements_by_tag_name('td')]
    film_data = {'название': name}
    value = ''
    key = ''
    for i in range(len(info)):
        if i % 2 != 0:
            value = info[i]
        else:
            key = info[i]
        if key in main_keys:
            film_data[key] = value
    return film_data


def correct_film_data(film_data):
    for key, value in film_data.items():
        if key == 'время':
            film_data[key] = int(re.match(r'\d+', value)[0])
        if '$' in value:
            film_data[key] = int(re.sub(r'[$ ]', '', value))
        if key == 'год':
            film_data[key] = int(value)
    return film_data


YEAR = 2018
MAIN_KEYS = ['год', 'страна', 'режиссер', 'сценарий',
             'композитор', 'жанр', 'бюджет', 'сборы в США',
             'сборы в России', 'время']
parse_films(YEAR, MAIN_KEYS)

# client = MongoClient('mongodb://127.0.0.1:27017')
# db = client['mail']
# mail_db = db.mail_ru
# mail_db.create_index('letter_id', unique=True)
