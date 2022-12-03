#!/usr/bin/python3

import argparse
import requests
import pprint
import yaml
import datetime as DT
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
                        to interact with wordpress: read, write')
    parser.add_argument('--data', action='store', help='use \
                        --data= with the following parameters \
                        to view wordpress rest api output in \
                        specified data format: json, yaml')
    args = parser.parse_args()
    varsargs = vars(args)
    try:
        argsvars = lower_argsvars(varsargs)
    except ParserError:
        return None, None
    except AttributeError:
        return None, None
    except OverflowError:
        return None, None
    except TypeError:
        return None, None
    if args.data:
        if args.data == "json":
            if args.blog == "read":
                return argsvars["blog"], argsvars["data"]
        if args.data == "yaml":
            if args.blog == "read":
                return argsvars["blog"], argsvars["data"]
        else:
            data = None
    if args.blog:
        if args.blog == "read":
            return argsvars["blog"], None
        if args.blog == "write":
            return argsvars["blog"], None
        else:
            pass
    else:
        return None, data


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

def yamlprint_r(r):  # pragma: no cover
    with open('./data/r.yaml', 'w') as f:
        yaml.dump(r, f, allow_unicode=True)
    with open('./data/r.yaml', 'r') as f:
        print(f.read())

def jsonprint_r(r):  # pragma: no cover
    PP = pprint.PrettyPrinter(indent=4)
    PP.pprint(r)

def get_iso_date():
    date = DT.datetime.now()
    iso_date = date.isoformat(timespec='seconds')
    return iso_date


def run_read(CREDS, data):  # pragma: no cover
    r = get_wp_r(CREDS)
    if r is None:
        print("Could not connect to wordpress.")
        exit()
    if data == "json":
        pprint_r(r)
        jsonprint_r(r)
        exit()
    if data == "yaml":
        yamlprint_r(r)
        exit()
    else:
        run_read_CLI(r)

def run_read_CLI(r):
    while True:
        print("Please supply parameters for how you would like to view your data: \
        json, yaml, \
        write (switch to write mode), \
        exit (quit Pyblog CLI)")
        CLI_input = input()
        if CLI_input == "json":
            jsonprint_r(r)
        if CLI_input == "yaml":
            yamlprint_r(r)
        else:
            if CLI_input == "write":
                run_write_CLI(CREDS)
            if CLI_input == "exit":
                exit()

def run_write_CLI(CREDS):
    post = {
        "status": "publish",
        "date": get_iso_date(),
        "categories": 1
        }
    while True:
        print("Please select from the following keys parameters \
              in order to supply a value in order to construct post data to send to wordpress: \
        title, content, post (show post data before publishing) \
        publish (post to wordpress)\
        read (switch to read mode), \
        exit (quit Pyblog CLI)")
        CLI_input = input()
        if CLI_input == "title":
            print("Provide title for your post:")
            CLI_input = input()
            post.setdefault("title", CLI_input)
        if CLI_input == "content":
            print("Provide content for your post:")
            CLI_input = input()
            post.setdefault("content", CLI_input)
        if CLI_input == "post":
            print(post)
        if CLI_input == "publish":
                try:
                    r = requests.post(CREDS["wp_posts_url"], auth=(CREDS["user"], CREDS["password"]), json=post)
                    if not r.status_code == 200:
                        print("Could not connect to wordpress.")
                except requests.exceptions.ConnectionError:
                    print("Could not connect to wordpress.")
                except requests.exceptions.Timeout:
                    print("Could not connect to wordpress.")
                print(r)
        else:
            if CLI_input == "read":
                data = None
                run_read(CREDS, data)
            if CLI_input == "exit":
                exit()



def run_pyblog():  # pragma: no cover
    blog, data = parse_args()
    if blog == "read":
        run_read(CREDS, data)
    if blog == "write":
        run_write_CLI(CREDS)
    else:
        print("Please specify --blog=read or --blog=write.  \
            Please use -h or --help on the command line \
                for more information on how to use Pyblog")


if __name__ == "__main__":
    run_pyblog()  # pragma: no cover
