import datetime
import zoneinfo


def get_current_datetime():

    current_dt = str(datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/London")))
    split_date = current_dt.split("-")
    split_time = split_date[2][3:len(split_date[2])].split(":")
    split_datetime = {
        "year": split_date[0],
        "month": split_date[1],
        "day": split_date[2][0:2],
        "hour": split_time[0],
        "min": split_time[1],
        "sec": split_time[2][0:2],
        "ms": split_time[2][3:len(split_time[2])]
    }
    return split_datetime

print(get_current_datetime())