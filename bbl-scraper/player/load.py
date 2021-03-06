#!/usr/bin/env python3
"""  Parse players from HTML"""
import sys
import os.path
import json
import logging
from bs4 import BeautifulSoup

from player import parse
from importer.bbleague.defaults import BASEPATH

LOG=logging.getLogger(__name__)


def from_file(filename):
    html = open(filename, "rb").read()
    soup = BeautifulSoup(html.decode("utf-8", 'ignore'), "html.parser")
    return soup


def parse_path(path):
    files = os.listdir(path)
    for player_file in filter(lambda f: f.startswith("player-"), files):
        playerid = player_file.replace("player-", "").replace(".html", "")
        yield parse.parse_fromfile(path, playerid)


def setup_log(level):
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)
    logging.addHandler(ch)


def write_json(player, path="input/json/player"):
    filename = "player-{}.json".format(player["playerid"])
    with open(os.path.join(path, filename), "w") as outfile:
        json.dump(player, outfile)


def load_player(path, filename):
    print("Open file {} {}".format(path, filename))
    with open(os.path.join(path, filename), "r") as infile:
        return json.load(infile)


def load(basepath=BASEPATH):
    path = os.path.join(basepath, "json/player/")
    files = os.listdir(path)
    for playerfile in filter(lambda f: f.startswith("player-") and f.endswith(".json"), files):
        yield load_player(path, playerfile)


def load_all():
    return load()


def main():
    if "--debug" in sys.argv[1:]:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Log level debug")

    do_print = True if "--no-print" not in sys.argv[1:] else False
    do_json = True if "--json" in sys.argv[1:] else False

    if "--load-all" in sys.argv[1:]:
        players = load_all()
        print("found {} players".format(sum(1 for x in players)))
        sys.exit()

    logging.basicConfig(level=logging.INFO)

    arguments = list(filter(lambda x: not x.startswith("--"), sys.argv[1:]))
    interesting = arguments if len(arguments) > 0 else None
    logging.info("program started")
    logging.debug("debug")
    # setup_log(logging.DEBUG)

    path = os.path.join(BASEPATH, "html/player/")
    logging.info("Loading players from %s", path)
    import pprint
    if interesting:
        logging.info("Looking for %s", interesting)
    pp = pprint.PrettyPrinter(indent=4)

    invalid_count = 0
    for player in parse_path(path):
        if not player:
            LOG.debug('Ignoring invalid file')
            invalid_count = invalid_count + 1
            continue
        if not interesting or player["playerid"] in interesting:
            if do_print:
                pp.pprint(player)
            if do_json:
                write_json(player=player, path=os.path.join(BASEPATH, "json/player/"))
    LOG.debug("%s invalid files", invalid_count)


if __name__ == "__main__":
    main()
