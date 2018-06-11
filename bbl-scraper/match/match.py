#!/usr/bin/env python3
import logging
from match import load
from match import parse

LOG = logging.getLogger(__package__)


def open_match(filename):
    matchid = filename[filename.find("match-") + 6:filename.rfind(".html")]

    return parse.parse_match(matchid, load.from_file(filename))


def collate_gamedata(games, id=None):
    LOG.debug("collate %s gamedata looking for %s", len(games), id if id else "last entry")
    return [m for m in games if m["matchid"] in id] if id else [games[-1]]


def dict_games():
    games = {}
    for g in match_list():
        games[g["matchid"]] = g
    return games


def match_list():
    games = load.from_json()
    return games
    import stats.collate
    data = stats.collate.collate()
    return data["game"].values() if "game" in data else load.from_json()


def main():
    import sys
    import pprint

    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    LOG.info("Loading matches")

    matchid = sys.argv[1:] if len(sys.argv) > 1 else None
    matches = list(collate_gamedata(match_list(), matchid))
    pprint.pprint(matches, indent=4, width=160)
    if len(sys.argv[1:]) > 1: print("Found {} of {}".format(len(matches), len(sys.argv[1:])))


if __name__ == "__main__":
    main()
