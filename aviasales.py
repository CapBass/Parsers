import requests
import json


def extract_value(json):
    try:
        return int(json['value'])
    except TypeError:
        return 0


def get_code(city, cities):
    for i in cities:
        if city == i['name']:
            return i['code']
    raise TypeError('invalid input')


def get_filght_tickets(start, end, cities, n):
    start = start.capitalize()
    end = end.capitalize()
    flight_params = {
        'origin': f'{get_code(start, cities)}',
        'destination': f'{get_code(end, cities)}',
        'one_way': 'true'
    }
    try:
        req = requests.get("http://min-prices.aviasales.ru/calendar_preload", params=flight_params)
    except:
        raise Exception('connection is unavailable ')

    data = req.json()['best_prices']
    data.sort(key=extract_value)
    return data[:n], start, end


def show_best_tickets(start, end, cities, n=5):
    tickets, start, end = get_filght_tickets(start, end, cities, n)

    print(f'Список из {n} наиболее дешевых билетов:')
    for ticket in tickets:
        price = ticket['value']
        date = ticket['depart_date']
        gate = ticket['gate']
        print(f'билет из города {start} в город {end} стоимостью {price} р. и датой вылета {date}. Компания {gate}')


cities = json.loads(requests.get('http://api.travelpayouts.com/data/ru/cities.json').content)

start = input('Введите город отправления ')
end = input('введите город назначения ')
show_best_tickets(start, end, cities)
