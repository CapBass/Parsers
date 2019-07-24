import collections
import requests
import re
import csv
from lxml import html
from urllib.parse import unquote


def return_wiki_html(topic):
    wiki_request = requests.get(f'https://ru.wikipedia.org/wiki/{topic.capitalize()}')
    return wiki_request.text


def get_links(topic):
    topic = topic.capitalize()
    page = requests.get(f'https://ru.wikipedia.org/wiki/{topic}')
    tree = html.fromstring(page.content)
    links = tree.xpath('//*[@id="mw-content-text"]//a/@href')
    links = set([link for link in links if '/wiki/' in link and '.png' not in link and '.jpg' not in link])
    return links


def return_words_from_links(link):
    topic = re.search(r'%.+', link)[0]
    wiki_html = return_wiki_html(topic)
    words = re.findall('[а-яА-Я]{3,}', wiki_html)
    words_counter = collections.Counter()
    for word in words:
        words_counter[word] += 1
    return words_counter.most_common(10), unquote(topic)


def write_words_from_topic_to_csv(counter, topic):
    # words = []
    # counts = []
    # for word, count in counter:
    #    words.append(word)
    #    counts.append(count)

    # data = [['Слово', 'Количество'],
    #        words,
    #        counts]
    name = f'{topic}.csv'
    name = re.sub('[!@#$/:;]', '', name)

    with open(name, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Word', 'Count'])
        for row in counter:
            writer.writerow(row)


def parse_topic_links(topic):
    links = get_links(topic)
    print(f'Всего из основного контента страницы {len(links)} внешних ссылок')
    for link in links:
        counter, topic = return_words_from_links(link)
        write_words_from_topic_to_csv(counter, topic)


parse_topic_links('Шарнир')
