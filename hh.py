import requests
import csv
from lxml import html
import os

headers = {'Accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}


def write_vacancies_to_csv(links, names, salaries, type):
    """
     Function writes data from hh page to csv
    """
    if type == 'vacancy':
        filename = 'vacancies.csv'
    else:
        filename = 'resumes.csv'
    data = zip(links, names, salaries)
    with open(filename, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        if os.stat(filename).st_size == 0:
            writer.writerow(['Ссылка', 'Наименование', 'Зарплата'])
        for row in data:
            writer.writerow(row)


def get_vacancies_from_page(page):
    """
     Function parses links, link names and salaries of vacancies from html page and saves it to lists
    """
    links = page.xpath('//div[contains(@class, "resume-search-item__name")]//a/@href')
    names = page.xpath('//div[contains(@class, "resume-search-item__name")]//a/text()')
    nodes = page.xpath('//div[contains(@class, "vacancy-serp-item__row vacancy-serp-item__row_header")]'
                       '/div[contains(@class, "vacancy-serp-item__sidebar")]')
    salaries = []
    for node in nodes:
        salary = node.xpath('.//div/text()')
        if salary:
            salaries.append(salary[0])
        else:
            salaries.append('NULL')

    return links, names, salaries


def get_resumes_from_page(page):
    """
     Function parses links and  link names of resume from html page and saves it to lists
    """
    urls = page.xpath('//div[contains(@class, "resume-search-item__header")]//a/@href')
    links = ['https://hh.ru' + url for url in urls]
    names = page.xpath('//div[contains(@class, "resume-search-item__header")]//a/text()')
    nodes = page.xpath('//div[contains(@class, "resume-search-item__header")]'
                       '/div[contains(@class, "resume-search-item__compensation")]')
    salaries = []
    for node in nodes:
        salary = node.xpath('./text()')
        if salary:
            salaries.append(salary[0])
        else:
            salaries.append('NULL')

    return links, names, salaries


def parse_hh(text, multi_page=True, n=5, type='vacancy'):
    """
     Function parses links, link names and salaries from hh and writes it to csv file
     text - search parameter (programming language)
     multi_page - if True, then this function will be parse n pages
     n - amount of pages
     type - vacancy or resume
    """
    params = {'text': text}
    session = requests.session()
    try:
        if type == 'vacancy':
            request = session.get('https://hh.ru/search/vacancy', headers=headers, params=params)
            page = html.fromstring(request.content)
            links, names, salaries = get_vacancies_from_page(page)
        else:
            request = session.get('https://khabarovsk.hh.ru/search/resume?'
                                  'logic=normal&pos=full_text&exp_period=all_time'
                                  '&clusters=true&order_by=relevance&no_magic=false', headers=headers, params=params)
            page = html.fromstring(request.content)
            links, names, salaries = get_resumes_from_page(page)
        write_vacancies_to_csv(links, names, salaries, type)
    except requests.exceptions.ConnectionError:
        print('Соединение не установлено')
        exit()

    if multi_page:  # parsing of n pages
        for i in range(n):
            url = page.xpath('//a[contains(@class, "bloko-button HH-Pager-Controls-Next HH-Pager-Control")]/@href')[0]
            url = 'https://hh.ru' + url
            request = session.get(url, headers=headers)
            page = html.fromstring(request.content)
            if type == 'vacancy':
                links, names, salaries = get_vacancies_from_page(page)
            else:
                links, names, salaries = get_resumes_from_page(page)
            write_vacancies_to_csv(links, names, salaries, type)
        session.close()
        return None
    else:
        session.close()
        return None


lang = input('Введите язык программирования ')
parse_hh(text=lang, multi_page=True, type='resume')
parse_hh(text=lang, multi_page=True, type='vacancy')
