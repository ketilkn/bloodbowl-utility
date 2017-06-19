#!/usr/bin/env python
from bs4 import BeautifulSoup
from unicodedata import normalize
import datetime
import re
from . import parse

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

def list_race():
    race = {}
    teams = list_teams()
    for t in teams:
        if t["race"] not in teams:
            race[t["race"]] = set() 
        race[t["race"]].add(t["id"])
    return race



def main():
    print(list_teams())
if __name__ == "__main__":
    main()
