import datetime
import time

import pandas as pd


def get_isotime(timestamp: float):
    return pd.Timestamp(timestamp, unit="s", tz="UTC").isoformat()


def the_time_in_iso_now_is():
    _now = datetime.datetime.utcnow()
    stamp: pd.Timestamp = \
        pd.Timestamp(_now.year, _now.month, _now.day, _now.hour, _now.minute, _now.second, _now.microsecond)
    return stamp.isoformat()


def the_time_now_is() -> float:
    _now = datetime.datetime.utcnow()
    stamp: pd.Timestamp = \
        pd.Timestamp(_now.year, _now.month, _now.day, _now.hour, _now.minute, _now.second, _now.microsecond)
    return stamp.timestamp()


def get_past_by_hour(interval: int = 1):
    _now = datetime.datetime.utcnow()
    stamp: pd.Timestamp = \
        pd.Timestamp(_now.year, _now.month, _now.day, _now.hour, _now.minute, _now.second, _now.microsecond)

    result: pd.Timestamp = stamp - pd.Timedelta(hours=interval)
    return result.timestamp()


def secs_until_next_oclock():
    this_hour: pd.Timestamp = pd.Timestamp.utcnow().replace(minute=0, second=0, microsecond=0)
    next_hour: pd.Timestamp = this_hour + pd.Timedelta(hours=1)
    delta: float = next_hour.timestamp() - time.time()
    return delta
