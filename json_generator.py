import random
import json
from faker import Faker
import time
import os
import datetime

fake = Faker()

# Write process id in file
with open('pid.txt', 'w') as f:
    f.write(str(os.getpid()))


# Main version test data
def log_example():
    logs_example = {
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
            {'{market_driver} monthly %': [8.0],
             '{market_driver}, daily %': [0.5],
             '{target_asset}, monthly %': [-2.0],
             '{target_asset}, daily %': [0.3],
             '{target_asset} RSI, daily': [0.8],
             '{target_asset} VWAP, daily': [0.279],
             '{target_asset} VWAP, hourly': [0.267],
             '{target_asset} volatility, daily': [0.3],
             '{target_asset} volatility, hourly': [0.03],
             '{target_asset} sentiment rate': [0.3],
             'Model-based historical accuracy': [0.63],
             'Model-based historical precision': [0.65],
             'Model-based historical recall': [0.61],
             'Dynamic Chi-squared test, p-value': [0.6]}}
    return logs_example


# Later version test data
def generate_random_data(time):
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
            {'{market_driver} monthly %': [8.0],
             '{market_driver}, daily %': [0.5],
             '{target_asset}, monthly %': [-2.0],
             '{target_asset}, daily %': [0.3],
             '{target_asset} RSI, daily': [0.8],
             '{target_asset} VWAP, daily': [0.279],
             '{target_asset} VWAP, hourly': [0.267],
             '{target_asset} volatility, daily': [0.3],
             '{target_asset} volatility, hourly': [0.03],
             '{target_asset} sentiment rate': [0.3],
             'Model-based historical accuracy': [0.63],
             'Model-based historical precision': [0.65],
             'Model-based historical recall': [0.61],
             'Dynamic Chi-squared test, p-value': [0.6]}}


if __name__ == '__main__':
    while True:
        dt = datetime.datetime.now()
        dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        with open("data.json", "w") as f:
            for i in range(1):
                data['charts'][0]['timestamp'].append(dt_str)
                data['charts'][0]['portfolio_value'].append(random.randint(2800, 3200))
                data['charts'][1]['timestamp'].append(dt_str)
                data['charts'][1]['price'].append(round(random.uniform(0.28, 0.30), 2))
                new_data = json.dumps(data, indent=4)
                f.write(new_data)
        time.sleep(2)



    # while True:
    #     dt = datetime.datetime.now()
    #     dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    #     with open("data.json", "r") as f:
    #         for i in range(1):
    #             data = json.load(f)
    #             data['charts'][0]['timestamp'].append(dt_str)
    #             data['charts'][0]['portfolio_value'].append(random.randint(2800, 3200))
    #             data['charts'][1]['timestamp'].append(dt_str)
    #             data['charts'][1]['price'].append(round(random.uniform(0.28, 0.30), 2))
    #             n = json.dumps(data, indent=4)
    #
    #     with open("data.json", "w") as f:
    #         f.write(n)
    #
    #     time.sleep(2)





#  For generate_random_data
# while True:
#     dt = datetime.datetime.now()
#     dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
#     with open("data.json", "a") as f:
#         for i in range(1):
#             data = generate_random_data(dt_str)
#             json_data = json.dumps(data)
#             f.write(json_data + "\n")
#     time.sleep(2)
