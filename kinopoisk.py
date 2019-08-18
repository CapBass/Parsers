from selenium import webdriver
import re
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def parse_films(year, main_keys):
    """
    Функция парсит данные с сайта кинопоиск и сохраняет в базу данных mongo
    :param year: год фильмов
    :param main_keys: ключи табличной части на странице фильма
    :return: записывает словарь данных в БД монго
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['films']
    films_db = db.films
    films_db.create_index('film_id', unique=True)
    driver = webdriver.Firefox()
    urls = get_urls_films_by_year(driver, year)
    for url in urls:
        film_data = correct_film_data(get_data_from_url(driver, url, main_keys))
        film_data['film_id'] = int(re.findall(r'\d+', url)[0])
        try:
            films_db.insert_one(film_data)
            print(f'Record {film_data["film_id"]} added')
        except DuplicateKeyError:
            print(f'Record {film_data["film_id"]} already exist')
            continue
        print(film_data)
    driver.close()


def get_urls_films_by_year(driver, year):
    """
    Функция получает ссылки на страницы фильмов соответтсвующего года
    :param driver: вебдрайвер firefox
    :param year: год фильмов
    :return: ссылки на страницы фильмов указанного года
    """
    driver.get(f'https://www.kinopoisk.ru/lists/navigator/{year}/?quick_filters=films')
    assert "КиноПоиск" in driver.title

    elements = driver.find_elements_by_class_name('selection-film-item-meta__link')
    urls = []
    for elem in elements:
        url = elem.get_attribute('href')
        urls.append(url)
    return urls


def get_data_from_url(driver, url, main_keys):
    """
    Функция получает сырые данных со страницы фильма на кинопоиске
    :param driver: вебдрайвер firefox
    :param url: ссылка на страницу фильма
    :param main_keys: поля табличной части, которые требуется сохранить
    :return: словарь данных о фильма
    """
    driver.get(url)
    # time.sleep(5)
    elem = driver.find_element_by_class_name('moviename-title-wrapper')
    name = elem.text
    elem = driver.find_element_by_class_name('rating_ball')
    total_rating = elem.text
    elem = driver.find_element_by_class_name('ratingCount')
    total_count = elem.text
    table = driver.find_element_by_xpath('//div[@class="movie-info__content"]//table')
    info = [item.text for item in table.find_elements_by_tag_name('td')]
    film_data = {'название': name, 'рейтинг': total_rating, 'кол-во проголосоваваших': total_count}
    value = ''
    key = ''
    for i in range(len(info)):
        # данные в табличной части хранятся в списке, где
        # четные элементы - ключи, нечетные - значения
        if i % 2 != 0:
            value = info[i]
        else:
            key = info[i]
        if key in main_keys:
            film_data[key] = value
    return film_data


def correct_film_data(film_data):
    """
    Функция корректрует данные в различных ключах
    :param film_data: словарь сырых данных о фильме
    :return: словарь содержащий обработанные данные
    """
    for key, value in film_data.items():
        if key == 'время':
            film_data[key] = int(re.match(r'\d+', value)[0])
        elif '$' in value:
            value = re.match(r'\d+', re.sub(r'[$ ]', '', value))[0]
            film_data[key] = int(value)
        elif key == 'рейтинг':
            film_data[key] = float(value)
        elif key == 'кол-во проголосоваваших':
            film_data[key] = int(''.join(value.split(' ')))
        elif key == 'год':
            film_data[key] = int(value)
        elif key in ['сценарий', 'жанр', 'композитор']:
            values = value.split(',')
            if '...' in values[-1]:
                value = ','.join(values[:len(values) - 1])
                film_data[key] = value
        else:
            continue

    return film_data


YEAR = 2018
MAIN_KEYS = ['год', 'страна', 'режиссер', 'сценарий',
             'композитор', 'жанр', 'бюджет', 'сборы в США',
             'сборы в России', 'время']
parse_films(YEAR, MAIN_KEYS)
