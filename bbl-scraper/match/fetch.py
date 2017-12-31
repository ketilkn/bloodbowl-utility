#!/bin/env python3
"""fetch all games from anarchy blood bowl league"""
from os import path
import sys
import urllib.request
from urllib.error import HTTPError
from time import sleep
from bs4 import BeautifulSoup
import logging

BASE_URL = "http://www.anarchy.bloodbowlleague.com/default.asp?p=m&m={}"
DATA_URL = "http://www.anarchy.bloodbowlleague.com/matchdata.asp?m={}"

LOG = logging.getLogger(__package__)


def parse_index():
    result = set()
    with open("input/html/index.html", "rb") as index_file:
        soup = BeautifulSoup(index_file.read(), 'html.parser')
        for anchor in soup.find_all('a'):
            if anchor.has_attr("href") and anchor["href"].startswith("default.asp?p=m&m="):
                href = anchor["href"]
                result.add(href[href.rfind("=")+1:])
    return result


def new_games():
    download_to("http://www.anarchy.bloodbowlleague.com/", "input/html/index.html")
    return parse_index()


def download_to(url, target):
    """Download match with url to target path"""
    try:
        with urllib.request.urlopen(url) as response:
            if response.geturl() == url:
                html = response.readlines()
                try:
                    open(target, "wb").writelines(html)
                    LOG.info(" Wrote {} to {}".format(url, target))
                except OSError:
                    LOG.error(" Failed writing {} to {}".format(url, target))
            else:
                print(" Server redirect {} to {}".format(url, response.geturl()))
    except HTTPError as error:
        html = error.readlines()
        open(target, "wb").writelines(html)
        LOG.warning(" Server error {} to {}".format(url, target))


def download_match(matchid):
        download_to(DATA_URL.format(matchid), "input/html/match/matchdata-{}.html".format(matchid))
        sleep(1)
        download_to(BASE_URL.format(matchid), "input/html/match/match-{}.html".format(matchid))
        sleep(3)


def is_match_downloaded(matchid):
    return path.isfile("input/html/match/matchdata-{}.html".format(matchid)) \
        and path.isfile("input/html/match/match-{}.html".format(matchid)) 


def download_matches(from_match, to_match):
    for matchid in range(from_match, to_match):
            download_match(matchid)


def force_download():
    return "--force" in sys.argv


def recent_matches(force=force_download()):
    """Download recent matches from host. If force is True existing matches will be downloaded again"""
    LOG.info("Fetch recent games")
    games = new_games()
    LOG.info(" {} recent game{} {}".format(len(games), "s" if len(games) != 1 else "",  games))
    for g in games:
        if not is_match_downloaded(g) or force:
            LOG.info("Downloading game {}".format(g))
            download_match(g)
        else:
            LOG.info("Game {} already downloaded use --force to reload".format(g))


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    LOG.debug("Command line arguments %s", sys.argv)
    LOG.info("Fetch match")

    if len(sys.argv) == 2 and sys.argv[1].isnumeric():
        download_match(sys.argv[1])
    elif len(sys.argv) == 3:
        from_match = int(sys.argv[1])
        to_match = int(sys.argv[2]) + 1
        download_matches(from_match, to_match)
    else:
        recent_matches()


if __name__ == "__main__":
    main()
