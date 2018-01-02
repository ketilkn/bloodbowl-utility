#!/usr/bin/env python
"""  Create list of coaches from team list for use when actual coach list is missing. """
import sys
import os.path
import logging

from .coach import parse
import team.parse
from importer.bbleague.defaults import BASEPATH

LOG = logging.getLogger(__package__)



def create_coach(nick, uid):
    coach = {'nick': nick,
             'email': nick,
             'naf': "",
             'role': "coach",
             'phone': "",
             'location': "Old World",
             'login': parse.NEVER_LOGGED_IN,
             'loggedin': True,
             'uid': str(uid)}

    if coach["login"] != parse.NEVER_LOGGED_IN:
        coach["loggedin"] = True

    return coach


def parse_teams(teams):
    coaches = set()

    for t in teams:
        LOG.debug("Team '%s', '%s' '%s'",
                  t["name"] if t["name"] else "No name",
                  t["coach"] if t["coach"] else "No coach",
                  t["co-coach"] if t["co-coach"] else "No co-coach")

        if t["coach"]:
            coaches.add(t["coach"])
        if t["co-coach"]:
            coaches.add(t["co-coach"])

    return [create_coach(coach, index+10000) for index, coach in enumerate(coaches)]


def data_exists(basepath = BASEPATH):
    file_path = basepath + "html/team/teams-8.html"
    exists = os.path.isfile(file_path)
    LOG.debug("%s that %s isfile", exists, file_path)
    return exists


def list_coaches(basepath = BASEPATH):
    LOG.debug("Retrieving coaches from team list")
    teams = team.parse.list_teams(basepath)
    LOG.debug("Found {} teams".format(len(teams)))
    coaches = parse_teams(teams)

    return coaches



def main():
    import sys
    from pprint import pprint
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    LOG.info("Parsing teamlist for coaches")

    path = sys.argv[1] if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]) else BASEPATH
    coaches = list_coaches(path)

    if "--no-print" not in sys.argv:
        pprint(coaches, indent=2)




if __name__ == "__main__":
    main()