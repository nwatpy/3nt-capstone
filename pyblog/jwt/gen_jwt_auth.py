#!/usr/bin/python3

import requests
import pprint
from dotenv import dotenv_values

CREDS = dotenv_values('.env')


def get_jwt_auth(CREDS):
    post = {
        "username": CREDS["user"],
        "password": CREDS["password"]
    }
    try:
        r = requests.post(CREDS["wp_jwt_auth_url"], json=post)
        print(r)
        if not r.status_code == 200:
            return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None
    r = r.json()
    return r


def pprint_r(r):  # pragma: no cover
    with open('./data/jwt-auth.json', 'w') as f:
        PP = pprint.PrettyPrinter(indent=4, stream=f)
        PP.pprint(r)


if __name__ == "__main__":  # pragma: no cover
    r = get_jwt_auth(CREDS)
    pprint_r(r)
