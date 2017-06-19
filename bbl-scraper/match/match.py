#!/usr/bin/env python3
import sys
from match import load
from match import parse

def open_match(filename):
    matchid = filename[filename.find("match-")+6:filename.rfind(".html")]
        
    return parse.parse_match( matchid, load.from_file(filename))


def collate_gamedata(games):
    return games[-1]


def dict_games():
    games = {}
    for g in match_list():
        games[g["matchid"]] = g
    return games

def match_list():
    games = load.from_json()
    return games 


def main():
    print(collate_gamedata(match_list()))
if __name__ == "__main__":
    main()
