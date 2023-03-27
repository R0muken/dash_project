import random
import json
from faker import Faker
import time
import os
import datetime
import argparse

# Arguments
parser = argparse.ArgumentParser(prog='Json_generator')

parser.add_argument('-c', '--count')
parser.add_argument('-a', '--asset')
parser.add_argument('-n', '--number')
parser.add_argument('-g', '--global')
parser.add_argument('-v', '--value')
parser.add_argument('-s', '--start')
parser.add_argument('-e', '--end')

args = parser.parse_args()


# Write process id in file
with open('pid.txt', 'w') as f:
    f.write(str(os.getpid()))

# Table data
table_data = ['{market_driver} monthly %',
              '{market_driver}, daily %',
              '{target_asset}, monthly %',
              '{target_asset}, daily %',
              '{target_asset} RSI, daily',
              '{target_asset} VWAP, daily',
              '{target_asset} VWAP, hourly',
              '{target_asset} volatility, daily',
              '{target_asset} volatility, hourly',
              '{target_asset} sentiment rate',
              'Model-based historical accuracy',
              'Model-based historical precision',
              'Model-based historical recall',
              'Dynamic Chi-squared test, p-value']


# Later version test data
def generate_random_data(time):
    fake = Faker()
    data = {
        "name": fake.name(),
        "age": random.randint(18, 65),
        "email": fake.email(),
        "date": time,
        "is_active": random.choice([True, False])
    }
    return data


data = {
    'charts':
        [
            {
                'name': 'pnl',
                'timestamp': [],
                'portfolio_value': []
            },
            {
                'name': '{target_asset}',
                'timestamp': [],
                'price': []
            }
        ],
    'markers_table':
        {
        }
}

if __name__ == '__main__':

    while True:
        dt = datetime.datetime.now()
        dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        with open("data.json", "r") as f:
            for i in range(1):
                data = json.load(f)
                data['charts'][0]['timestamp'].append(dt_str)
                data['charts'][0]['portfolio_value'].append(random.randint(2800, 3200))
                data['charts'][1]['timestamp'].append(dt_str)
                data['charts'][1]['price'].append(round(random.uniform(0.28, 0.30), 2))

                data["markers_table"][random.choice(table_data)] = [round(random.uniform(0.1, 0.8), 2)]
                json_data = json.dumps(data, indent=4)

        with open("data.json", "w") as f:
            f.write(json_data)

        time.sleep(2)


