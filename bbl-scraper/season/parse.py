#!/usr/bin/env python
from bs4 import BeautifulSoup
from unicodedata import normalize
import datetime
import dateutil.parser as parser
import re
import list_teams_by_games
import coach.coach
#import team 
import sys

def id_from_onclick(el):
    if el and el.has_attr("onclick"):
        return el["onclick"][el["onclick"].find("'")+1:el["onclick"].rfind("'")]
    return "teamid not found {}".format(el.name)

def parse_team(team):
        team = { "name": team.text.replace(u"\xa0", ' '),
                 "teamid": id_from_onclick(team) }
        return team
def convert_to_isodate(text):
        return parser.parse(text).isoformat()

def parse_date(soup):
        found = soup.find_all("div")
        for div in found:
                if div.has_attr("align") and div.text.startswith("Result added"):
                        return convert_to_isodate(div.text.strip()[13:])
        return None
def parse_league(soup):
    league = {}
    for found in soup.select('tr td[style="color:#203040"]'):
        team = parse_team(found)
        league[team["teamid"]] = team
    return league
    


def open_league(filename):
        html = open(filename, "rb").read()
        soup = BeautifulSoup(html, "html.parser")
        league = parse_league(soup)
        return league 

def main():
    pass
if __name__ == "__main__":
    main()
