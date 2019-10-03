#!/usr/bin/env python3
import requests
import sys
import logging

LOG = logging.getLogger(__package__)

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'


def download_to(session, url, target):
    LOG.debug("Downloading %s to %s", url, target)
    response = session.get(url)
    if not response.history or response.status_code==200: 
        html = response.text
        try:
            open(target, "w").write(html)
            LOG.debug(" Wrote {} to {}".format(url, target))
            return True
        except OSError:
            LOG.error(" Failed writing {} to {}".format(url, target))
    else:
        LOG.error(" Server error {} to {}".format(url, response.status_code))
    return False


def verify_session(session, response = None):
    #TODO check if session is logged in
    LOG.debug("verifying session on %s", response.url)
    return response.status_code == 200 and response.url.endswith("/default.asp?p=adm")


def login(url, username, password):
    LOG.debug("Logging in to %s using %s", url, username)
    s = requests.session()
    r = s.post(url, headers={'Accept': ACCEPT, 'User-Agent': USER_AGENT}, data={"user":username, "pass":password})

    if verify_session(s, r):
        return s
    LOG.error("Could not verify session")
    print(r.content)
    sys.exit("Could not verify session")


def new_session():
    return requests.session()


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    session=login("http://www.anarchy.bloodbowlleague.com/login.asp", sys.argv[1], sys.argv[2])
    print("{}".format(session.cookies))


if __name__ == "__main__":
    main()
