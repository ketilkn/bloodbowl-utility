#!/usr/bin/env python
"""  Import data from bloodbowlleague.com """
import sys
import logging

import scrape.fetch_teamlist
import scrape.fetch_coachlist
import match.fetch

LOG = logging.getLogger(__package__)


def load_config(section):
    import configparser
    config = configparser.ConfigParser()
    LOG.debug("Loading config from bbl-scrape.ini")
    config.read("bbl-scrape.ini")
    if section not in config.sections():
       LOG.error("No such section %s in bbl-scrape.ini", section)
       sys.exit("Giving up")
    return config[section]


def import_bloodbowlleague(config):
    """Import data from host"""
    LOG.info("Importing data from %s", config.get("base_url"))

    scrape.fetch_teamlist.download_team_list(base_url=config.get("base_url"),
                                             username=config.get("username"),
                                             password=config.get("password"),
                                             base_path=config.get("base_path"))

    scrape.fetch_coachlist.download_coach_list(base_url=config.get("base_url"),
                                               username=config.get("username"),
                                               password=config.get("password"),
                                               base_path=config.get("base_path"))
    match.fetch.recent_matches(base_url=config.get("base_url"),
                               base_path=config.get("base_path"),
                               force=True)


def testing():
    pass
    #teams = team_list.parse(load(
        #fetch(cache("http://example.com/t={}", "team/{}", "mot"),
              #session=session(username, password, "http://example.com/login"))))

    #teams = team_list.parse(fetch("http://www.anarchy.bloodbowlleague.com/default.asp?p=te", "teamlist.html")))

def main():
    """Run import_bloodbowlleague from command line"""
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    import_bloodbowlleague(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()