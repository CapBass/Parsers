import requests
import re
import csv
from lxml import html

headers = {'Accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}


def get_tree_by_text(text, area=None):
    params = {'text': text, 'area': area}
    session = requests.session()
    request = session.get('https://hh.ru/search/vacancy', headers=headers, params=params)
    tree = html.fromstring(request.content)
    size = max(tree.xpath('//a[contains(@class, "bloko-button")]/@data-page'))
    for i in size[:5]:
        links = tree.xpath('//div[contains(@class, "resume-search-item__name")]//a/@href')
        names = tree.xpath('//div[contains(@class, "resume-search-item__name")]//a/text()')

        return links, names


print(get_tree_by_text('Python'))
