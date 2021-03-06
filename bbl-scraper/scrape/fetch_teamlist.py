#!/bin/env python3
import sys
import os.path
import logging
import scrape.session

LOG = logging.getLogger(__package__)

teams_script = "default.asp?p=te"


def download(session, url, path):
    pass


def download_team_list(base_url, username, password, base_path):
    LOG.debug("Download teamlist from %s to %s", base_url, base_path)
    s = scrape.session.login("{}/login.asp".format(base_url), username=username, password=password)
    target_path = os.path.join(base_path, "html", "team")
    if not os.path.isdir(target_path):
        LOG.warning("Target path %s does not exist. Attempting to create", base_path)
        os.makedirs(target_path)

    teams_location = "{}/{}".format(base_url, teams_script)
    scrape.session.download_to(s, teams_location, os.path.join(base_path, "html/team/teams-8.html"))


def main():
    import argparse
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    parser = argparse.ArgumentParser()

    parser.add_argument("username")
    parser.add_argument("password")
    parser.add_argument("base_url")
    parser.add_argument("base_path")

    arguments = parser.parse_args()

    download_team_list(arguments.base_url,  arguments.username,  arguments.password, arguments.base_path) 


if __name__ == "__main__":
    main()
