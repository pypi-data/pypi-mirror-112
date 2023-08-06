import http.client
import json
from typing import TypedDict

PROD_HOST = "engine.pathlit.io"
weights_path = "/v1/optimiser/weights"
paths_path = "/v1/optimiser/paths"
sims_path = "/v1/optimiser/sims"


class DataPoint(TypedDict):
    date: str
    value: float


class TimeSeries(TypedDict):
    name: str
    data: list[DataPoint]


class Client:
    """A HTTP client for the PathLit APIs.

    :param api_key: your API key obtained from the PathLit dashboard

    Example::

        from pathlit.client import Client

        c = Client("YOUR_API_KEY")
        c.simulate(["AAPL", "AMZN", "NVDA", "QQQ"])
    """
    def __init__(self, api_key: str):
        self.header = {"x-api-key": api_key}
        self.host = PROD_HOST

    def get_weights(self, tickers: list[str]) -> dict[str, list[float]]:
        """Computes the weights to be allocated for a portfolio, under different strategies. 

        See https://www.pathlit.io/docs/api/weights for more information.

        :param tickers: a list of ticker strings
        """
        req_body = json.dumps({"tickers": tickers})
        s = self.__fetch(weights_path, req_body)
        res = json.loads(s)
        return res

    def get_paths(self, tickers: list[str]) -> list[TimeSeries]:
        """Computes the dollar returns of a 100,000 USD portfolio according
        to the weights computed by `get_weights`.

        See https://www.pathlit.io/docs/api/paths for more information.

        :param tickers: a list of instrument tickers
        """
        req_body = json.dumps({"tickers": tickers})
        s = self.__fetch(paths_path, req_body)
        d = json.loads(s)

        return [parse_time_series(dc) for dc in d]

    def simulate(self, tickers: list[str], run_count=10) -> list[list[TimeSeries]]:
        """Computes the dollar returns of a 100,000 USD portfolio according 
        to the weights computed by `get_weights`, but across simulated (normally-distributed) 
        market data. 
        
        See https://www.pathlit.io/docs/api/sims for more information.

        :param tickers: a list of instrument tickers
        :param run_count: the number of simulated market data universes. Defaults to 10.
        """
        req_body = json.dumps({"tickers": tickers, "run_count": run_count})
        resp_body = self.__fetch(sims_path, req_body)
        return parse_sims(resp_body)

    def __fetch(self, path: str, body: str) -> str:
        conn = http.client.HTTPSConnection(self.host)
        conn.request("POST", path, body, headers=self.header)
        s = conn.getresponse().read().decode()
        conn.close()
        return s


def parse_time_series(d: dict) -> TimeSeries:
    name = d["PATH"]
    res: TimeSeries = {"name": name, "data": []}
    for k, v in d.items():
        if k == "PATH":
            continue
        p: DataPoint = {"date": k, "value": float(v)}
        res["data"].append(p)
    return res


def parse_sims(input_str: str) -> list[list[TimeSeries]]:
    d = json.loads(input_str)
    res = []
    for i, run in d.items():
        res.append(list(map(lambda allocation: parse_time_series(allocation), run)))
    return res
