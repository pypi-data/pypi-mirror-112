import json
import requests

def btcprice(currency):
    return str(requests.get("https://blockchain.info/ticker").json()[currency]["last"])


def convert(usdvolume):
    return str(usdvolume / requests.get("https://blockchain.info/ticker").json()["USD"]["last"])

