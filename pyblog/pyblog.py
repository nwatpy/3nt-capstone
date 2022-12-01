#!/usr/bin/python3

import requests
import json
from dotenv import dotenv_values
import pprint

CREDS = dotenv_values(".env")

def get_wp_response(CREDS):
    try:
        response = requests.get(CREDS["wp_posts_url"], auth=(CREDS["user"], CREDS["password"]))
        if not response.status_code == 200:
            return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None
    response_data = response.json()
    return response_data

def pprint_response_data(response_data):
    with open('./data/response_data.json', 'w') as f:
        PP = pprint.PrettyPrinter(indent=4, stream=f)
        PP.pprint(response_data)

if __name__ == "__main__":
    response_data = get_wp_response(CREDS); pprint_response_data(response_data)