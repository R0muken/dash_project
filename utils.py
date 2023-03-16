# Transformation input from full name to arg name
def transformation(value):
    if value == 'count':
        return '-c'
    if value == 'value':
        return '-v'
    if value == 'number':
        return '-n'
    if value == 'global':
        return '-g'
    return value


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