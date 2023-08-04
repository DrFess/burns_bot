import datetime

from db.commands import get_urine_per_time, get_weight


def indicators_per_time(case, date, some_function):
    indicator = some_function(case, date)
    total_indicator = 0
    for item in indicator:
        total_indicator += item[0]
    return total_indicator


def calculate_date(hours: str):
    delta = datetime.timedelta(hours=float(hours))
    search_date = datetime.datetime.now() - delta
    return search_date


def calculate_hydrobalance(case, date, time):
    diuresis = indicators_per_time(case, date, get_urine_per_time)
    weight = get_weight(case)
    result = round(diuresis / weight / time, 2)
    return result
