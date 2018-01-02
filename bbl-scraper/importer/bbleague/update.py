#!/usr/bin/env python
"""  Import data from bloodbowlleague.com """
import sys
import logging

import scrape.fetch_teamlist
import scrape.fetch_coachlist
import match.fetch

LOG = logging.getLogger(__package__)


def import_bloodbowlleague(host, username, password):
    """Import data from host"""
    LOG.info("Importing data from %s", host)

    scrape.fetch_teamlist.download_team_list(username, password)
    scrape.fetch_coachlist.download_coach_list(username, password)
    match.fetch.recent_matches()


def main():
    """Run import_bloodbowlleague from command line"""
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    import_bloodbowlleague(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()