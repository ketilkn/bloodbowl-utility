#!/usr/bin/env python3
""" Python libraries for Dr.Tide"""
import logging
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
    logging.addHandler(ch)

def main():
    print(__package__)
    print(__name__)

    if "--debug" in sys.argv[1:]:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Log level debug")

    do_print = True if "--no-print" not in sys.argv[1:] else False

    logging.basicConfig(level=logging.INFO)

    arguments = list(filter(lambda x: not x.startswith("--"), sys.argv[1:]))
    interesting = arguments if len(arguments) > 0 else None
    logging.info("program started")
    logging.debug("debug")
    #setup_log(logging.DEBUG)

    path = "input/html/player/"
    logging.info("Loading players from %s", path)
    import pprint
    if interesting:
        logging.info("Looking for %s", interesting)
    pp = pprint.PrettyPrinter(indent=4)

    for player in parse_path(path):
        if do_print and (not interesting or player["playerid"] in interesting):
            pp.pprint(player)

if __name__ == "__main__":
    main()
