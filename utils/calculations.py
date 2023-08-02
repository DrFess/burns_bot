from db.commands import get_urine, get_weight


def calculate_hydrobalance(case, date, time):
    diuresis_per_time = get_urine(case, date)
    diuresis = 0
    for item in diuresis_per_time:
        diuresis += item[0]
    weight = get_weight(case)
    result = round(diuresis / weight / time, 2)
    return result
