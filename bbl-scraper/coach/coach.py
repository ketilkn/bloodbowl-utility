#!/usr/bin/env python
import sys
import os
import json
import logging
from coach import parse
import coach.parse_from_team
from importer.bbleague.defaults import BASEPATH

LOG = logging.getLogger(__package__)


def dict_coaches(use_key="nick"):
    coaches = list_coaches()
    result = {}
    for coach in coaches:
        result[coach[use_key]] = coach
        # result[coach["uid"]] = coach
    return result


def dict_coaches_by_uid():
    return dict_coaches("uid")


def load_from_json(basepath = BASEPATH):
    LOG.debug("Loading %sjson/coaches.json", basepath)
    data = open(basepath + "json/coaches.json", "rb").read()
    return json.loads(data.decode())


def save_to_json(coaches, basepath = BASEPATH):
    LOG.debug("Saving %s/json/coaches.json", basepath)
    data = json.dumps(coaches)
    json_file = open(basepath+"json/coaches.json", "wb")
    json_file.write(data.encode())
    json_file.close()


def load_from_parser(basepath = BASEPATH):
    LOG.debug("Loading from parser")
    if parse.data_exists(basepath):
        LOG.debug("Found data for parse")
        return parse.load(basepath)
    elif coach.parse_from_team.data_exists(basepath):
        LOG.debug("Found data for parse_from_team")
        return coach.parse_from_team.list_coaches(basepath)
    LOG.error("Found no usable coach data")


def list_coaches(basepath = BASEPATH):
    if not os.path.isfile(basepath + "json/coaches.json") or (
            os.path.isfile(basepath + "html/coach/coaches-8.html") and os.stat(basepath + "json/coaches.json").st_mtime < os.stat(
            basepath + "html/coach/coaches-8.html").st_mtime):
        coaches = load_from_parser(basepath)
        save_to_json(coaches, basepath)
        return coaches
    return load_from_json(basepath)


def find_uid_for_nick(coaches, nick):
    for the_coach in coaches.values():
        if the_coach["nick"] == nick:
            return the_coach["uid"]
    return None
    # return [key for key, value in coaches if value["nick"] == nick]


def parse_options():
    LOG.debug("Options: %s ", sys.argv)
    if len(sys.argv) < 2:
        LOG.debug("Less than 2 options")
        return BASEPATH, None
    if os.path.isdir(sys.argv[1]):
        LOG.debug("Argument 1 is a directory")
        return sys.argv[1], sys.argv[2:] if len(sys.argv) > 2 else None
    LOG.debug("Argument 1 is not a directory")

    return BASEPATH, sys.argv[1:]

    #= sys.argv[1] if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]) else "input/bloodbowlleague/anarchy.bloodbowlleague.com/"
    #search_options = sys.argv[1:] if not os.path.isdir(sys.argv[1]) else sys.argv[2:]


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    basepath, search_options = parse_options()
    LOG.debug("%s :: %s", basepath, search_options)

    LOG.info("Loading coaches")

    coaches = list_coaches(basepath)
    for coach in coaches:
        if not search_options or coach["nick"] == " ".join(search_options) or coach["nick"] in search_options or coach[ "uid"] in search_options:
            print(coach)
    print("Total: {}".format(len(coaches)))


if __name__ == "__main__":
    main()
