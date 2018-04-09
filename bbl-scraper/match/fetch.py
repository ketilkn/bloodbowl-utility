#!/bin/env python3
"""fetch all games from anarchy blood bowl league"""
import os.path
import sys
import urllib.request
from urllib.error import HTTPError
from time import sleep
from bs4 import BeautifulSoup
import logging
from importer.bbleague.defaults import BASEPATH

BASE_URL = "{}/default.asp?p=m&m={}"
DATA_URL = "{}/matchdata.asp?m={}"

LOG = logging.getLogger(__package__)


def parse_index(basepath=BASEPATH):
    result = set()
    with open(os.path.join(basepath, "html", "index.html"), "rb") as index_file:
        soup = BeautifulSoup(index_file.read(), 'html.parser')
        for anchor in soup.find_all('a'):
            if anchor.has_attr("href") and anchor["href"].startswith("default.asp?p=m&m="):
                href = anchor["href"]
                result.add(href[href.rfind("=")+1:])
    return result


def new_games(base_path=BASEPATH, base_url="http://www.anarchy.bloodbowlleague.com/"):
    download_to(base_url, os.path.join(base_path, "html", "index.html"))
    return parse_index(base_path)


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


def download_match(matchid, directory=BASEPATH, base_url="http://www.anarchy.bloodbowlleague.com"):
        download_to(DATA_URL.format(base_url, matchid), os.path.join(directory, "html/match/", "matchdata-{}.html".format(matchid)))
        sleep(1)
        download_to(BASE_URL.format(base_url, matchid), os.path.join(directory, "html/match/", "match-{}.html".format(matchid)))
        sleep(3)


def is_match_downloaded(matchid, directory=BASEPATH+"html/match/"):
    return os.path.isfile(os.path.join(directory, "matchdata-{}.html".format(matchid))) \
        and os.path.isfile(os.path.join(directory, "match-{}.html".format(matchid)))


def download_matches(basepath, from_match, to_match):
    for matchid in range(from_match, to_match):
            download_match(matchid, basepath)


def force_download():
    return "--force" in sys.argv


def recent_matches(base_url="http://www.anarchy.bloodbowlleague.com/", base_path = BASEPATH, force=force_download()):
    """Download recent matches from host. If force is True existing matches will be downloaded again"""
    LOG.info("Fetch recent games")
    games = new_games(base_path, base_url)
    LOG.info(" {} recent game{} {}".format(len(games), "s" if len(games) != 1 else "",  games))
    target_path = os.path.join(base_path, "match")

    if not os.path.isdir(target_path):
        LOG.warning("Target path %s does not exist. Attempting to create", target_path)
        os.makedirs(target_path)

    for g in games:
        if not is_match_downloaded(g, base_path) or force:
            LOG.info("Downloading game {}".format(g))
            download_match(g, directory=base_path, base_url=base_url)
        else:
            LOG.info("Game {} already downloaded use --force to reload".format(g))


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    LOG.debug("Command line arguments %s", sys.argv)
    LOG.info("Fetch match")

    basepath = sys.argv[1] if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]) else BASEPATH

    if len(sys.argv) == 3 and sys.argv[2].isnumeric():
        download_match(sys.argv[2], basepath)
    elif len(sys.argv) == 4:
        from_match = int(sys.argv[2])
        to_match = int(sys.argv[3]) + 1
        download_matches(basepath, from_match, to_match)
    else:
        recent_matches(basepath)


if __name__ == "__main__":
    main()
