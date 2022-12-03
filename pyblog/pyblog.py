#!/usr/bin/python3

import argparse
import requests
import pprint
import yaml
import json
import ruamel.yaml
import datetime as DT
from dotenv import dotenv_values
from sys import exit

CREDS = dotenv_values('.env')


def parse_args():  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="CLI for wordpress REST API. \
            Pyblog written by Team N3T from the IEA Cohort 08. \
            Special thanks to the instructor JR Rickerson")
    parser.add_argument('--blog', action='store', help='use \
                        --blog= with the following parameters \
                        to interact with Pyblog CLI: read, write')
    parser.add_argument('--data', action='store', help='use \
                        --data= with the following parameters \
                        to view and save wordpress rest api output in \
                        specified data format: json, yaml \
                        Example: --blog=read --data=json')
    args = parser.parse_args()
    varsargs = vars(args)
    try:
        argsvars = lower_argsvars(varsargs)
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
    if args.blog:
        if args.blog == "read":
            return argsvars["blog"], None
        if args.blog == "write":
            return argsvars["blog"], None
    else:
        return None, None


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


def remove_links_yaml():
    with open('./data/r.yaml', 'r') as f:
        clean_yaml = ruamel.yaml.round_trip_load(f)
    with open('./data/clean.yaml', 'w') as f:
        del clean_yaml[0]["_links"]
        del clean_yaml[1]["_links"]
        del clean_yaml[2]["_links"]
        del clean_yaml[3]["_links"]
        del clean_yaml[4]["_links"]
        ruamel.yaml.round_trip_dump(clean_yaml, stream=f, block_seq_indent=1)


def get_post_template(r):
    with open('./data/cleaner.yaml', 'w') as f:
        yaml.dump(r, f, allow_unicode=True)


def display_post_template():
    with open('./data/cleaner.yaml', 'r') as f:
        print(f.read())


def remove_links_json(r):
    keys = '_links'
    return {k: v for k, v in r[0].items() if k not in keys}


def jsonprint_r(r):  # pragma: no cover
    r = remove_links_json(r)
    with open('./data/clean.json', 'w') as f:
        PP = pprint.PrettyPrinter(indent=4, stream=f)
        PP.pprint(r)
    get_post_template(r)
    PP = pprint.PrettyPrinter(indent=4)
    PP.pprint(r)


def get_date():  # pragma: no cover
    date = DT.datetime.now()
    return date.isoformat(timespec='seconds')


def run_read(CREDS, data):  # pragma: no cover
    r = get_wp_r(CREDS)
    if r is None:
        print("Could not connect to wordpress.")
        exit()
    if data == "json":
        pprint_r(r)
        jsonprint_r(r)
        print("Displaying newest post data.\
        Entire response saved to ./data/r.json")
        exit()
    if data == "yaml":
        yamlprint_r(r)
        remove_links_yaml()
        r = remove_links_json(r)
        get_post_template(r)
        display_post_template()
        print("Displaying newest post data.\
        Entire response saved to ./data/r.yaml\
        Clean response saved to ./data/clean.yaml\
        Post Template saved to ./data/cleaner.yaml")
        exit()
    else:
        run_read_CLI(r)


def run_read_CLI(r):
    while True:
        print("Choose how to display data:\
        json, yaml\
        write (switch to write mode)\
        exit (quit Pyblog CLI)")
        CLI_input = input()
        if CLI_input.lower() == "json":
            pprint_r(r)
            jsonprint_r(r)
            print("Displaying newest post data.\
            Entire response saved to ./data/r.json")
        if CLI_input.lower() == "yaml":
            yamlprint_r(r)
            remove_links_yaml()
            r = remove_links_json(r)
            get_post_template(r)
            display_post_template()
            print("Displaying newest post data.\
            Entire response saved to ./data/r.yaml\
            Clean response saved to ./data/clean.yaml\
            Post Template saved to ./data/cleaner.yaml")
        else:
            if CLI_input.lower() == "write":
                run_write_CLI(CREDS)
            if CLI_input.lower() == "exit":
                exit()


def run_write_CLI(CREDS):
    post = {
        "date": get_date(),
        "status": "publish",
        "format": "standard"
    }
    while True:
        print("Please select from the following:\
        title (create title for your post)\
        content (write your post)\
        post (show post data before publishing)\
        publish (post to wordpress)\
        template (publishes designated template file)\
        read (switch to read mode)\
        exit (quit Pyblog CLI)")
        CLI_input = input()
        if CLI_input.lower() == "title":
            print("Provide title for your post:")
            CLI_input = input()
            post.setdefault("title", CLI_input)
        if CLI_input.lower() == "content":
            print("Provide content for your post:")
            CLI_input = input()
            post.setdefault("content", CLI_input)
        if CLI_input.lower() == "post":
            print(post)
        if CLI_input.lower() == "publish":
            wp_publish(post)
        if CLI_input.lower() == "template":
            print("Provide filepath to template:")
            CLI_input = input()
            with open(CLI_input, 'r') as f:
                post_template = yaml.safe_load(f)
            with open('./data/post_template_json', 'w') as f:
                json.dump(post_template, f)
            with open('./data/post_template_json', 'r') as f:
                post_template = json.load(f)
            post.setdefault("title", post_template["title"])
            post.setdefault("content", post_template["content"])
            wp_publish(post)

        else:
            if CLI_input.lower() == "read":
                data = None
                run_read(CREDS, data)
            if CLI_input.lower() == "exit":
                exit()


def wp_publish(post):
    curHeaders = {
        "Authorization": "Bearer %s" % CREDS["jwt_auth"],
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    try:
        r = requests.post(CREDS["wp_posts_url"], headers=curHeaders, json=post)
        if not r.status_code == 201:
            print("Post failed.\
            Possible issue with connection or credentials.")
            return
        else:
            print("Data successfully posted to wordpress.")
            return
    except requests.exceptions.ConnectionError:
        print("Could not connect to wordpress.")
    except requests.exceptions.Timeout:
        print("Could not connect to wordpress.")


def run_pyblog():  # pragma: no cover
    blog, data = parse_args()
    if blog == "read":
        run_read(CREDS, data)
    if blog == "write":
        run_write_CLI(CREDS)
    else:
        print("Please specify --blog=read or --blog=write. \
        Please use -h or --help for more information on this tool")


if __name__ == "__main__":
    run_pyblog()  # pragma: no cover
