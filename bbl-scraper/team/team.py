#!/usr/bin/env python
from bs4 import BeautifulSoup
from unicodedata import normalize
import datetime
import re
from . import parse
import collections

def dict_teams():
    teams = list_teams()
    result = {}
    for team in teams:
        result[team["id"]] = team
    return result

def list_teams():
        html = open("input/teams-8.html", "r").read()
        soup = BeautifulSoup(normalize("NFC", html), "html.parser")

        teams = parse.parse_rows( parse.find_rows(soup))
        return teams    

def list_race(collated_data=None):
    race = collections.defaultdict(set)
    teams = list_teams() if collated_data==None else collated_data["team"].values()
    for t in teams:
        race[t["race"]].add(t["id"])
    return race

#Fix me. merge list_race, filter_race 
def filter_race(collated_data):
    race = collections.defaultdict(set)
    for teamid, team in collated_data["team"].items():
        print(team)
        race[team["race"]].add(team["id"])
    return race

def main():
    import sys
    import pprint
    for t in list_teams():
        if len(sys.argv) < 2 or t["id"] in sys.argv[1:]:
            pprint.pprint(t, indent=4, width=200)
if __name__ == "__main__":
    main()
