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
            {}
    }
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
        {
        }
}

if __name__ == '__main__':
    # with open("data.json", "w") as f:
    #     new_data = json.dumps(data, indent=4)
    #     f.write(new_data)

    # while True:
    #     dt = datetime.datetime.now()
    #     dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    #     with open("logs-example.json", "w") as f:
    #         for i in range(1):
    #             data['charts'][0]['timestamp'].append(dt_str)
    #             data['charts'][0]['portfolio_value'].append(random.randint(2800, 3200))
    #             data['charts'][1]['timestamp'].append(dt_str)
    #             data['charts'][1]['price'].append(round(random.uniform(0.28, 0.30), 2))
    #             # new_data = json.dumps(data, indent=4)
    #             # f.write(new_data)
    #     time.sleep(2)

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
                n = json.dumps(data, indent=4)

        with open("data.json", "w") as f:
            f.write(n)

        time.sleep(2)

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
