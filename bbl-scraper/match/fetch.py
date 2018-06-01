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
                    LOG.debug(" Wrote {} to {}".format(url, target))
                except OSError:
                    LOG.error(" Failed writing {} to {}".format(url, target))
            else:
                LOG.error(" Server redirect {} to {}".format(url, response.geturl()))
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


def download_matches(basepath, from_match, to_match, force=True):
    download_matches2(base_path=basepath, games=list(range(from_match, to_match)), force=force)


def force_download():
    return "--force" in sys.argv


def download_matches2(base_url="http://www.anarchy.bloodbowlleague.com/", base_path=BASEPATH, force=force_download(), games=[]):
    target_path = os.path.join(base_path, "match")

    if not os.path.isdir(target_path):
        LOG.warning("Target path %s does not exist. Attempting to create", target_path)
        os.makedirs(target_path)

    for g in games:
        if not is_match_downloaded(g, base_path) or force:
            LOG.info("Downloading match {}".format(g))
            download_match(g, directory=base_path, base_url=base_url)
        else:
            LOG.debug("Match {} already downloaded use --force to reload".format(g))


def recent_matches(base_url="http://www.anarchy.bloodbowlleague.com/", base_path = BASEPATH, force=force_download()):
    """Download recent matches from host. If force is True existing matches will be downloaded again"""
    LOG.debug("Fetch recent matches")
    games = new_games(base_path, base_url)
    LOG.info("{} recent match{} {}".format(len(games), "es" if len(games) != 1 else "",  games))

    download_matches2(base_url, base_path=base_path, force=force, games=games)


def main():
    import importer.bbleague.update
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    LOG.debug("Command line arguments %s", sys.argv)
    LOG.info("Fetch match")

    site = sys.argv[1] if len(sys.argv) > 1 else "anbbl"
    config = importer.bbleague.update.load_config(site)

    if len(sys.argv) == 3 and sys.argv[2].isnumeric():
        download_match(sys.argv[2], config.get("base_path"))
    elif len(sys.argv) == 4:
        from_match = int(sys.argv[2])
        to_match = int(sys.argv[3]) + 1
        download_matches(config.get("base_path"), from_match, to_match)
    else:
        recent_matches(base_path=config.get("base_path"))


if __name__ == "__main__":
    main()
