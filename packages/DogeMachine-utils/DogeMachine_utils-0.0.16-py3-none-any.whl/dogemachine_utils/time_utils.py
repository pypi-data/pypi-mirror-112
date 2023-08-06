from datetime import date
import time


def get_year_month_day_string() -> str:
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    return d1


def get_current_time_string() -> str:
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time


def get_current_time_z_string() -> str:
    t = time.localtime()
    current_time = time.strftime("%H-%MZ", t)
    return current_time
