import json
import os

import urllib3
import certifi

pool = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


def get_program_list():
	program_list = [p.replace(".json", "") for p in os.listdir("data/programs")]
	return program_list


def get_json(file: str) -> dict:
	data = json.load(open(file))
	return data


def get_remote_json(url: str) -> dict:
	response = pool.request("GET", url)
	return json.loads(response.data.decode("utf-8"))
