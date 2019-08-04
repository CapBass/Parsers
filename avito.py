import requests
from lxml import html
from pymongo import MongoClient
import pymongo
from pprint import pprint


def request_avito(region='habarovsk'):
    request_str = f'https://www.avito.ru/{region}/avtomobili'
    try:
        responce = requests.get(request_str).text
    except requests.exceptions.ConnectionError:
        print('Соединение не установлено')
        exit(1)
    avito_html = html.fromstring(responce)
    items = avito_html.xpath('//div[@data-item-id or @class="serp-vips-item "]')
    return items


def save_to_mongo_db():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['avito']
    avito_db = db.avito_auto
    # avito_db.drop()
    avito_db.create_index('auto_id', unique=True)

    items = request_avito()
    for item in items:
        auto_id = item.xpath('.//@id')[0]
        link = 'https://www.avito.ru' + item.xpath('.//a[contains(@itemprop, "url")]/@href')[0]
        name, age = item.xpath('.//span[@itemprop="name"]/text()')[0].split(',')
        price = item.xpath('.//*[@itemprop="price"]/@content')[0]
        data_avito_auto = {
            'auto_id': auto_id,
            'link': link,
            'name': name,
            'age': int(age),
            'price': int(price)
        }
        try:
            avito_db.insert_one(data_avito_auto)
            print(f'Record {auto_id} added')
        except pymongo.errors.DuplicateKeyError:
            print(f'Record {auto_id} already exist')
            continue


def get_from_mongo_by_price(price):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['avito']
    avito_db = db.avito_auto
    result = avito_db.find({'price': {'$lt': price}})
    for i in result:
        pprint(i)


save_to_mongo_db()
get_from_mongo_by_price(500000)
