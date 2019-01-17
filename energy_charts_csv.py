# Usage 1: python energy_charts_csv.py 06.2015 [15|30]
# Usage 2: python energy_charts_csv.py W4.2015 [15|30]

import urllib.request
import sys
import json
import pandas as pd
import datetime


def json_fn_from_args(args):
    resolution = int(args[2]) if len(args) >= 3 and (args[2] == '15' or args[2] == '30') else None
    res_str = f'{resolution}min_' if resolution is not None else ''
    parts = args[1].split('.')
    year = parts[1]
    if parts[0].startswith('W'):
        week = parts[0].replace('W', '')
        week = '0' + week if len(week) == 1 else week
        return f'week_{res_str}{year}_{week}.json'
    else:
        month = parts[0]
        month = '0' + month if len(month) == 1 else month
        return f'month_{res_str}{year}_{month}.json'


def url_from_args(args):
    return f'https://www.energy-charts.de/price/{json_fn_from_args(args)}'


def slurp_url(url):
    with urllib.request.urlopen(url) as response:
        return response.read()


def get_second(list_of_pairs, first):
    for pair in list_of_pairs:
        if pair[0] == first:
            return pair[1]
    return -1

def timestamp_readable(ts):
    return datetime.datetime.fromtimestamp(int(ts)/1000.0).strftime('%Y-%m-%d %A %H:%M:%S.%f')

def main(args):
    obj = json.loads(slurp_url(url_from_args(args)))
    col_names = [entry['key'][0]['en'] for entry in obj]
    index = [pair[0] for pair in obj[0]['values']]
    data = [[timestamp_readable(row_ix)]+[get_second(obj[col_ix]['values'], row_ix) for col_ix in range(len(col_names))] for row_ix in index]
    df = pd.DataFrame(data, index=index, columns=['datetime']+col_names)
    df.to_csv(f'converted_{args[1].replace(".", "_")}.csv', index_label='timestamp')


if __name__ == '__main__':
    main(sys.argv)
