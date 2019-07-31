from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

date_dict = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12'
}


def request_news(region):
    request_str = f'https://news.yandex.ru/{region}'
    try:
        responce = requests.get(request_str).text
    except requests.exceptions.ConnectionError:
        print('Соединение не установлено')
        exit()
    soup = BeautifulSoup(responce, 'html.parser')
    news_html = soup.findAll('div', {'class': re.compile('^story story_view')})
    return news_html


def get_date(text_data, date_dict):
    clean_text = ' '.join(text_data.split())
    date_parse = re.findall('\s[^в ]+|вчера', clean_text)
    today = datetime.today().strftime("%d %m %Y").split()
    year = '2019'

    if len(date_parse) == 1:
        day = today[0]
        month = today[1]
        time = date_parse[0].strip()
    elif len(date_parse) == 2:
        day = int(today[0]) - 1
        month = today[1]
        time = date_parse[1].strip()
    else:
        day = date_parse[0].strip()
        month = date_dict[date_parse[1].strip()]
        time = date_parse[2].strip()

    date = datetime.strptime(f'{day} {month} {year} {time}', '%d %m %Y %H:%M')

    return date


def get_news_list(news_html):
    news = []
    for story in news_html:
        story_data = {}
        story_html = story.findAll(['div', 'h2', 'a'],
                                   {'class': re.compile('(story__(info|text|title)|rubric-label_top)')})
        story_data['category'] = story_html[0].text
        link = 'https://news.yandex.ru' + story_html[1].find('a').attrs['href']
        story_data['link'] = link
        story_data['title'] = story_html[1].text
        story_data['text'] = story_html[2].text
        try:
            story_data['date'] = get_date(story_html[3].text, date_dict)
        except IndexError:
            story_data['text'] = None
            story_data['date'] = get_date(story_html[2].text, date_dict)

        news.append(story_data)

    news = sorted(news, key=lambda k: k['category'])
    return news


def split_news_by_category(news):
    news_split_list = []
    category = news[0]['category']
    start = 0
    end = 0
    for idx, value in enumerate(news):
        if value['category'] != category:
            end = idx
            category_news = sorted(news[start:end], key=lambda k: k['date'])
            news_split_list.append(category_news)
            start = end
        category = value['category']
    return news_split_list


def show(news_split_list):
    for news_list in news_split_list:
        category = news_list[0]['category']
        print(f'Рубрика "{category}"')
        print()
        for news in news_list:
            print(news['title'])
            if news['text']:
                print(news['text'])
            print(news['link'])
            print(news['date'].__format__('%d %m %Y %H:%M'))
            print()


def parse(region='Khabarovsk'):
    news_html = request_news(region)
    news = get_news_list(news_html)
    news_split_list = split_news_by_category(news)
    show(news_split_list)


parse()
