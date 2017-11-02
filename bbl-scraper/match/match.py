#!/usr/bin/env python3
import sys
from match import load
from match import parse

def open_match(filename):
    matchid = filename[filename.find("match-")+6:filename.rfind(".html")]
        
    return parse.parse_match( matchid, load.from_file(filename))


def collate_gamedata(games, id=None):
    return [m for m in games if m["matchid"] == id][0] if id else games[-1]


def dict_games():
    games = {}
    for g in match_list():
        games[g["matchid"]] = g
    return games

def match_list():
    games = load.from_json()
    return games 


def main():
    import sys
    import pprint
    matchid = sys.argv[1] if len(sys.argv) > 1 else None
    pprint.pprint(collate_gamedata(match_list(), matchid), indent=4, width=160)
if __name__ == "__main__":
    main()
