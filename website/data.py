import json
import urllib3
import certifi

pool = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


def getJson(file: str) -> dict:
    data = json.load(open(file))
    return data


def get_remote_json(url: str) -> dict:
    response = pool.request("GET", url)
    return json.loads(response.data.decode("utf-8"))
