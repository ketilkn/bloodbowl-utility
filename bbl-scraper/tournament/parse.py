#!/usr/bin/env python
import sys
from bs4 import BeautifulSoup
import logging


def id_from_onclick(el):
    if el and el.has_attr("onclick"):
        return el["onclick"][el["onclick"].find("'")+1:el["onclick"].rfind("'")]
    return "teamid not found {}".format(el.name)


def parse_team(team):
    team_name = team
    team = { "name": team_name.text.replace(u"\xa0", ' '),
             "teamid": id_from_onclick(team_name) }
    return team


def parse_standings(soup):
    standings = []
    for position, found in enumerate(soup.select('tr td[style="color:#203040"]')):
        team = parse_team(found)
        team["position"]=position+1
        standings.append(team)
    return standings
    

def open_standings(filename):
        html = open(filename, "rb").read()
        soup = BeautifulSoup(html, "html.parser")
        league = parse_standings(soup)
        return league 


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    tournament = open_standings(sys.argv[1])
    for t in tournament:
        print(t)



if __name__ == "__main__":
    main()

