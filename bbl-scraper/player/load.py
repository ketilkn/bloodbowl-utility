#!/usr/bin/env python3
""" Python libraries for Dr.Tide"""
import logging
LOG = logging.getLogger(__name__)
from bs4 import BeautifulSoup
from unicodedata import normalize
import datetime
import dateutil.parser as parser
import re
#import team 
import sys
from os import listdir
import os.path

from player import parse

def from_file(filename):
        plyerid = filename[filename.find("player-")+6:filename.rfind(".html")]
        html = open(filename, "rb").read()
        soup = BeautifulSoup(html, "html.parser")
        return soup

def parse_path(path):
    files = os.listdir(path)
    for player_file in filter(lambda f: f.startswith("player-"), files):
        playerid = player_file.replace("player-","").replace(".html","")
        yield parse.parse_fromfile(path, playerid)


def setup_log(level):
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)
    LOG.addHandler(ch)

def main():
    print(__package__)
    print(__name__)
    LOG.setLevel(logging.INFO)
    setup_log(logging.DEBUG)
    arguments = sys.argv[1:]
    if "--debug" in arguments:
        arguments.remove("--debug")
        LOG.setLevel(logging.DEBUG)
        LOG.debug("Log level debug")
        print("debug???")
    else:
        print("itte debug")
    interesting = arguments if len(sys.argv) > 0 else None

    path = "input/html/player/"
    LOG.info("Loading players from %s", path)
    import pprint
    if interesting:
        LOG.info("Looking for %s", interesting)
    pp = pprint.PrettyPrinter(indent=4)

    for player in parse_path(path):
        if not interesting or player["playerid"] in interesting:
            pp.pprint(player)

if __name__ == "__main__":
    main()
