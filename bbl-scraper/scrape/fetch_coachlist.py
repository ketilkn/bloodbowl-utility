#!/bin/env python3
import sys
import os.path
import scrape.session
import logging

LOG = logging.getLogger(__name__)

coaches_url = "/default.asp?p=co"


def download_coach_list(base_url, username, password, base_path):
    login_url = "{}/login.asp".format(base_url)
    s = scrape.session.login(login_url, username=username, password=password)
    source_url = "{}/{}".format(base_url, coaches_url)

    target_path = os.path.join(base_path, "html/coach")

    if not os.path.isdir(target_path):
        LOG.warning("Target path %s does not exist. Attempting to create", target_path)
        os.makedirs(target_path)

    scrape.session.download_to(s, source_url, os.path.join(target_path, "coaches-8.html"))


def main():
    download_coach_list("http://www.anarchy.bloodbowlleague.com", sys.argv[1], sys.argv[2], "input/anarchy.bloodbowlleague.com")


if __name__ == "__main__":
    main()
