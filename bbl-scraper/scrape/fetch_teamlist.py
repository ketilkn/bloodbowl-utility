#!/bin/env python3
import sys
import requests
from time import sleep
import scrape.session

teams_url = "http://www.anarchy.bloodbowlleague.com/default.asp?p=te"
	
def download_team_list():
    s = scrape.session.login(sys.argv[1], sys.argv[2])
    scrape.session.download_to(s, teams_url, "input/teams-8.html")
	
def main():
    download_team_list()

if __name__ == "__main__":
    main()
