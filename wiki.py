import collections
import requests
import re
import csv
from lxml import html



def return_wiki_html(topic):
    wiki_request = requests.get(f'https://ru.wikipedia.org/wiki/{topic.capitalize()}')
    return wiki_request.text


def get_links(topic):
    topic = topic.capitalize()
    page = requests.get(f'https://ru.wikipedia.org/wiki/{topic}')
    tree = html.fromstring(page.content)
    links = tree.xpath('//a[@class=\"external text\"]/@href')
    links = [link for link in links if 'http' in link]
    names = tree.xpath('//a[@class=\"external text\"]/text()')
    return links, names


def return_words_from_links(link):
    try:
        html = requests.get(link).text
    except:
        print(f'Соединение c {link} не установлено')
        return None
    words = re.findall('[а-яА-Я]{3,}', html)
    words_counter = collections.Counter()
    for word in words:
        words_counter[word] += 1
    return words_counter.most_common(10)


def write_words_from_topic_to_csv(counter, names):
    for name in names:
        with open(name + '.csv', mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Word', 'Count'])
            for row in counter:
                writer.writerow(row)


def parse_topic_links(topic):
    links, names = get_links(topic)
    print(f'Всего из основного контента страницы {len(links)} внешних ссылок')
    for link in links:
        counter = return_words_from_links(link)
        if counter:
            write_words_from_topic_to_csv(counter, names)


parse_topic_links('Матрац')
