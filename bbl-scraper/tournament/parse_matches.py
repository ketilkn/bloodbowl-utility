#!/usr/bin/env python
import sys
from bs4 import BeautifulSoup
import logging

LOG = logging.getLogger(__name__)


def id_from_onclick(el):
    if el and el.has_attr("onclick"):
        return el["onclick"][el["onclick"].rfind("=")+1:el["onclick"].rfind("'")]
    return "teamid not found {}".format(el.name)


def parse_match(match):
    return id_from_onclick(match)


def parse_matches(soup):
    standings = []
    matches = soup.findAll(lambda t: t.name=="tr" and t.has_attr("onclick") and t["onclick"].startswith("self.location.href='default.asp?p=m&m="))
    #matches = soup.findAll(lambda t: t.name=="tr" and t.has_attr("title") and t["title"].startswith("result added"))
    LOG.debug("Found %s matches", len(matches))
    for found in matches:
        team = parse_match(found)
        standings.append(team)
    return standings
    

def open_matches(filename):
        html = open(filename, "rb").read()
        soup = BeautifulSoup(html, "html.parser")
        matches = parse_matches(soup)
        return matches


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    matches = open_matches(sys.argv[1])
    for m in matches:
        print(m)


if __name__ == "__main__":
    main()

