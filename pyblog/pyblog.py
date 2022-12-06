#!/usr/bin/python3

import argparse
import requests
import pprint
import yaml
import json
import os
import ruamel.yaml
import datetime as DT
from dotenv import load_dotenv
from sys import exit

load_dotenv()
CREDS = os.environ


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
    parser.add_argument('--template', action='store', help='use \
                        --blog=write --template=<filepath> \
                        to post template file to wordpress instantly. \
                        use --blog=write --data=plain --template=<filepath> \
                        to post plain text file to wordpress instantly')
    args = parser.parse_args()
    varsargs = vars(args)
    if args.template is not None and args.data is None:
        if args.blog == "write":
            return varsargs["blog"], None, varsargs["template"]
    if args.template is not None and args.data == "plain":
        if args.blog == "write":
            if args.data == "plain":
                return varsargs["blog"], varsargs["data"], varsargs["template"]
    try:
        argsvars = lower_argsvars(varsargs)
    except AttributeError:
        return None, None, None
    except OverflowError:
        return None, None, None
    except TypeError:
        return None, None, None
    if args.data:
        if args.data == "json":
            if args.blog == "read":
                return argsvars["blog"], argsvars["data"], None
        if args.data == "yaml":
            if args.blog == "read":
                return argsvars["blog"], argsvars["data"], None
    if args.blog:
        if args.blog == "read":
            return argsvars["blog"], None, None
        if args.blog == "write":
            return argsvars["blog"], None, None
    else:
        return None, None, None


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


def parse_post_id():
    with open('./data/cleaner.yaml', 'r') as f:
        post_id = yaml.safe_load(f)
    with open('./data/parse_post_id.json', 'w') as f:
        json.dump(post_id, f)
    with open('./data/parse_post_id.json', 'r') as f:
        post_id = json.load(f)
    return int(post_id["id"])


def yaml_clean_print(post_id):
    with open('./data/r.yaml', 'r') as f:
        clean_yaml = ruamel.yaml.round_trip_load(f)
    with open('./data/clean.yaml', 'w+') as f:
        x = 0
        try:
            for clean_yaml[0]["_links"] in range(1, post_id):
                del clean_yaml[x]["_links"]
                x += 1
        except IndexError:
            ruamel.yaml.round_trip_dump(
                clean_yaml, stream=f, block_seq_indent=1)


def get_cleaner_yaml(r):
    with open('./data/cleaner.yaml', 'w') as f:
        yaml.dump(r, f, allow_unicode=True)


def display_cleaner_yaml():
    with open('./data/cleaner.yaml', 'r') as f:
        print(f.read())


def remove_links_json(r):
    keys = '_links'
    return {k: v for k, v in r[0].items() if k not in keys}


def jsonprint_r(r):  # pragma: no cover
    try:
        r = remove_links_json(r)
    except KeyError:
        pass
    with open('./data/clean.json', 'w') as f:
        PP = pprint.PrettyPrinter(indent=4, stream=f)
        PP.pprint(r)
    get_cleaner_yaml(r)
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
        try:
            r = remove_links_json(r)
        except KeyError:
            pass
        get_cleaner_yaml(r)
        post_id = parse_post_id()
        try:
            yaml_clean_print(post_id)
        except KeyError:
            pass
        display_cleaner_yaml()
        print("Displaying newest post data.\
        Entire response saved to ./data/r.yaml\
        Clean response saved to ./data/clean.yaml\
        yaml data displayed saved to ./data/cleaner.yaml")
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
            try:
                r = remove_links_json(r)
            except KeyError:
                pass
            get_cleaner_yaml(r)
            post_id = parse_post_id()
            try:
                yaml_clean_print(post_id)
            except KeyError:
                pass
            display_cleaner_yaml()
            print("Displaying newest post data.\
            Entire response saved to ./data/r.yaml\
            Clean response saved to ./data/clean.yaml\
            yaml data displayed saved to ./data/cleaner.yaml")
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
            PP = pprint.PrettyPrinter(indent=4)
            PP.pprint(post)
        if CLI_input.lower() == "publish":
            wp_publish(post)
        if CLI_input.lower() == "template":
            print("Is template file yaml or plain text? Type yaml or plain:")
            CLI_input = input()
            if CLI_input == "yaml":
                print("Provide filepath to template:")
                CLI_input = input()
                post_template = load_template(CLI_input)
                post.setdefault("title", post_template["title"])
                post.setdefault("content", post_template["content"])
                wp_publish(post)
            if CLI_input == "plain":
                print("Provide filepath to template:")
                CLI_input = input()
                template = CLI_input
                publish_plaintext(template)

        else:
            if CLI_input.lower() == "read":
                data = None
                run_read(CREDS, data)
            if CLI_input.lower() == "exit":
                exit()


def load_template(CLI_input):
    with open(CLI_input, 'r') as f:
        post_template = yaml.safe_load(f)
    with open('./data/post_template.json', 'w') as f:
        json.dump(post_template, f)
    with open('./data/post_template.json', 'r') as f:
        post_template = json.load(f)
    return post_template


def publish_template(template):
    post = {
        "date": get_date(),
        "status": "publish",
        "format": "standard"
    }
    with open(template, 'r') as f:
        post_template = yaml.safe_load(f)
    with open('./data/post_template.json', 'w') as f:
        json.dump(post_template, f)
    with open('./data/post_template.json', 'r') as f:
        post_template = json.load(f)
    post.setdefault("title", post_template["title"])
    post.setdefault("content", post_template["content"])
    wp_publish(post)


def publish_plaintext(template):
    post = {
        "date": get_date(),
        "status": "publish",
        "format": "standard"
    }
    with open(template, 'r') as f:
        lines = f.readlines()
        post_template = [line.strip() for line in lines]
    post.setdefault("title", post_template.pop(0))
    post_template = '\n '.join(post_template)
    post.setdefault("content", post_template)
    wp_publish(post)


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
        return
    except requests.exceptions.Timeout:
        print("Could not connect to wordpress.")
        return


def run_pyblog():  # pragma: no cover
    blog, data, template = parse_args()
    if blog == "read":
        run_read(CREDS, data)
    if blog == "write" and template is None:
        run_write_CLI(CREDS)
    if blog == "write" and data is None and template is not None:
        publish_template(template)
    if blog == "write" and data == "plain" and template is not None:
        publish_plaintext(template)
    else:
        print("Please specify --blog=read or --blog=write. \
        Please use -h or --help for more information on this tool")


if __name__ == "__main__":
    run_pyblog()  # pragma: no cover
