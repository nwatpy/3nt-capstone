#!/usr/bin/python3

import argparse
import requests
import pprint
from dotenv import dotenv_values
from sys import exit
from parser import ParserError

CREDS = dotenv_values('.env')


def parse_args():  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="CLI for wordpress REST API.  \
            Pyblog written by Team N3T from the IEA Cohort 08.")
    parser.add_argument('--blog', action='store', help='use \
                        --blog= with the following parameters \
                            to interact with wordpress: \
                            read, write')
    args = parser.parse_args()
    varsargs = vars(args)
    try:
        argsvars = lower_argsvars(varsargs)
    except ParserError:
        return None
    except AttributeError:
        return None
    except OverflowError:
        return None
    except TypeError:
        return None
    if args.blog:
        if args.blog == "read" or args.blog == "write":
            return argsvars["blog"]
        else:
            pass
    else:
        return None


def lower_argsvars(varsargs):  # pragma: no cover
    for i in varsargs.keys():
        varsargs[i] = varsargs[i].lower()
        return varsargs


def get_wp_r(CREDS):
    try:
        r = requests.get(CREDS["wp_posts_url"], auth=(
            CREDS["user"], CREDS["password"]))
        if not r.status_code == 200:
            return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None
    r = r.json()
    return r


def pprint_r(r):  # pragma: no cover
    with open('./data/r.json', 'w') as f:
        PP = pprint.PrettyPrinter(indent=4, stream=f)
        PP.pprint(r)


def read_wp(r):  # pragma: no cover
    PP = pprint.PrettyPrinter(indent=4)
    PP.pprint(r)


def run_read(CREDS):  # pragma: no cover
    r = get_wp_r(CREDS)
    if r is None:
        print("Could not connect to wordpress.")
        exit()
    else:
        pprint_r(r)
        read_wp(r)


def run_pyblog():  # pragma: no cover
    blog = parse_args()
    if blog is not None:
        if blog == "read":
            run_read(CREDS)
    else:
        print("Please specify --blog=read or --blog=write.  \
            Please use -h or --help on the command line \
                for more information on how to use Pyblog")


if __name__ == "__main__":
    run_pyblog()  # pragma: no cover
