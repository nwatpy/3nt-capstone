#!/usr/bin/python3

import requests
import json
import base64
from dotenv import dotenv_values
import pprint

creds = dotenv_values(".env")

def get_wp_response():
    credentials = creds["user"] + ':' + creds["password"]
    token = base64.b64encode(credentials.encode())
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}
    try:
        response = requests.get(creds["wp_posts_url"] , headers=header)
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
    response_data = get_wp_response(); pprint_response_data(response_data)