#!/usr/bin/env python
import os
import json
import logging
from coach import parse
import coach.parse_from_team

LOG = logging.getLogger(__package__)


def dict_coaches(use_key="nick"):
    coaches = list_coaches()
    result = {}
    for coach in coaches:
        result[coach[use_key]] = coach
        #result[coach["uid"]] = coach
    return result

def dict_coaches_by_uid():
    return dict_coaches("uid")

def load_from_json():
    LOG.debug("Loading input/json/coaches.json")
    data = open("input/json/coaches.json", "rb").read()
    return json.loads(data.decode())


def save_to_json(coaches):
    data = json.dumps(coaches)
    json_file = open("input/json/coaches.json", "wb")
    json_file.write(data.encode())
    json_file.close()

def load_from_parser():
    LOG.debug("Loading from parser")
    if parse.data_exists():
        LOG.debug("Found data for parse")
        return parse.load()
    elif coach.parse_from_team.data_exists():
        LOG.debug("Found data for parse_from_team")
        return coach.parse_from_team.list_coaches()
    LOG.error("Found no useable coach data")

def list_coaches():
    if not os.path.isfile("input/json/coaches.json") or (os.path.isfile("input/html/coach/coaches-8.html") and os.stat("input/json/coaches.json").st_mtime < os.stat("input/html/coach/coaches-8.html").st_mtime):
        coaches = load_from_parser()
        save_to_json(coaches)
        return coaches
    return load_from_json()


def find_uid_for_nick(coaches, nick):
    for the_coach in coaches.values():
        if the_coach["nick"] == nick:
            return the_coach["uid"]
    return None
    #return [key for key, value in coaches if value["nick"] == nick]

def main():
    import sys

    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    LOG.info("Loading coaches ")

    coaches = dict_coaches_by_uid()
    for coach in coaches.values():
        if len(sys.argv) < 2 or coach["nick"]==" ".join(sys.argv[1:]) or coach["nick"] in sys.argv[1:] or coach["uid"] in sys.argv[1:]:
            print (coach)
    print("Total: {}".format(len(coaches)))

if __name__ == "__main__":
    main()
