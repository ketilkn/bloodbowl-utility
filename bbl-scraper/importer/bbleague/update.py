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
    LOG.info("Loading config from bbl-scrape.ini using %s", section)
    config.read("bbl-scrape.ini")
    if section not in config.sections():
       LOG.error("No such section %s in bbl-scrape.ini", section)
       sys.exit("Giving up")
    return config[section]


def import_bbleague(config):
    """Import teamlist, coaches and recent match data from host"""
#   LOG.info("Importing data %s to %s", config.get("base_url"), config.get("base_path"))
    LOG.info("Importing data")
    LOG.info("base_url   %s", config.get("base_url"))
    LOG.info("base_path  %s", config.get("base_path"))


    LOG.info("Update teams")
    scrape.fetch_teamlist.download_team_list(base_url=config.get("base_url"),
                                             username=config.get("username"),
                                             password=config.get("password"),
                                             base_path=config.get("base_path"))

    LOG.info("Update coaches")
    scrape.fetch_coachlist.download_coach_list(base_url=config.get("base_url"),
                                               username=config.get("username"),
                                               password=config.get("password"),
                                               base_path=config.get("base_path"))
    LOG.info("Update recent matches")
    match.fetch.recent_matches(base_url=config.get("base_url"),
                               base_path=config.get("base_path"),
                               force=True)


def main():
    """Run import_bloodbowlleague from command line"""
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    import_bbleague(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
