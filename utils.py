import json


# Transformation input from full name to arg name
def transformation(value):
    argument = '-'+value[0]
    return argument


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


# Reading assets from txt file
def asset_retrieving(file):
    asset_options = []
    with open(f'{file}', 'r') as f:
        for line in f:
            line = line.strip()
            asset_options.append(line)
    return asset_options


# Reading data from file
def data_retrieving():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data
