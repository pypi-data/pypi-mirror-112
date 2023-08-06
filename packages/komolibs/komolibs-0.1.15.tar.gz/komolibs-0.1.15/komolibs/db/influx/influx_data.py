from datetime import datetime

from typing import Any

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxData:
    def __init__(self, url: str, org: str, token: str):
        self._client = InfluxDBClient(url=url, token=token)
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
        self._org = org

    def write(self, bucket: str, point: Point):
        self._write_api.write(bucket, self._org, point)

    def batch(self, bucket: str, sequence: Any):
        self._write_api.write(bucket, self._org, sequence)

    def query(self, query: str):
        return self._client.query_api().query(query, org=self._org)
