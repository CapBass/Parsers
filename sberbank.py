import matplotlib.pyplot as plt
import csv


def append_to_data(values, dates, row, start, end):
    if start and end:
        if (row['date'] >= start) and (row['date'] <= end):
            dates.append(row['date'])
            values.append(int(row['value']))
    elif start:
        if row['date'] >= start:
            dates.append(row['date'])
            values.append(int(row['value']))
    elif end:
        if row['date'] <= end:
            dates.append(row['date'])
            values.append(int(row['value']))
    else:
        dates.append(row['date'])
        values.append(int(row['value']))


def get_open_data(name=None, region=None, start=None, end=None):
    with open('opendata.csv', 'r') as f:
        reader = csv.DictReader(f)
        values = []
        dates = []
        for row in reader:
            if name and region:
                if row['name'] == name and row['region'] == region:
                    append_to_data(values, dates, row, start, end)
            elif name:
                if row['name'] == name:
                    append_to_data(values, dates, row, start, end)
            elif region:
                if row['region'] == region:
                    append_to_data(values, dates, row, start, end)
            else:
                append_to_data(values, dates, row, start, end)

    plt.plot(dates, values)
    plt.xticks(dates)
    plt.show()


NAME = 'Средняя сумма заявки на потребительский кредит'
REGION = 'Хабаровский край'
START = '2018-01-01'
END = '2019-01-01'
get_open_data(NAME, REGION, START, END)
