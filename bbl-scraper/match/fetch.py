#!/bin/env python3
"""fetch all games from anarchy blood bowl league"""
import urllib.request
from urllib.error import HTTPError
from time import sleep
from bs4 import BeautifulSoup

BASE_URL = "http://www.anarchy.bloodbowlleague.com/default.asp?p=m&m={}"
DATA_URL = "http://www.anarchy.bloodbowlleague.com/matchdata.asp?m={}"

def parse_index():
    result = set()
    with open("input/index.html", "rb") as index_file:
        soup = BeautifulSoup(index_file.read(), 'html.parser')
        for anchor in soup.find_all('a'):
            if anchor.has_attr("href") and anchor["href"].startswith("default.asp?p=m&m="):
                href = anchor["href"]
                result.add(href[href.rfind("=")+1:])
    return result

def new_games():
    download_to("http://www.anarchy.bloodbowlleague.com/", "input/index.html")
    return parse_index()



def download_to(url, target):
    try:
        with urllib.request.urlopen(url) as response:
            if response.geturl() == url:
                html = response.readlines()
                try:
                    open(target, "wb").writelines(html)
                    print("Wrote {} to {}".format(url, target))
                except OSError:
                    print("Failed writing {} to {}".format(url, target))
            else:
                print("Server redirect {} to {}".format(url, response.geturl()))
    except HTTPError as error:
        html = error.readlines()
        open(target, "wb").writelines(html)
        print("Server error {} to {}".format(url, target))
def download_match(matchid):
    download_to(DATA_URL.format(matchid), "input/matchdata-{}.html".format(matchid))
    sleep(1)
    download_to(BASE_URL.format(matchid), "input/match-{}.html".format(matchid))
    sleep(3)

def download_matches(from_match, to_match):
    for matchid in range(from_match, to_match):
        download_match(matchid)

def main():
    import sys
    if len(sys.argv) == 2:
        download_match(sys.argv[1])
    elif len(sys.argv) == 3:
        from_match = int(sys.argv[1])
        to_match = int(sys.argv[2]) + 1
        download_matches(from_match, to_match)
    else:
        for m in new_games():
            download_match(m)

if __name__ == "__main__":
    main()