#!/bin/env python3
import sys
import requests
from time import sleep
import scrape.session

base_url = "http://www.anarchy.bloodbowlleague.com/default.asp?p=pl&pid={}"
admin_url = "http://www.anarchy.bloodbowlleague.com/default.asp?p=pladm&pid={}"
	
def download_all_players(fetch_list):
    s = scrape.session.login("http://www.anarchy.bloodbowlleague.com/login.asp",sys.argv[1], sys.argv[2])
    for playerid in fetch_list:
        if scrape.session.download_to(s, admin_url.format(playerid), "input/admin-player-{}.html".format(playerid)):
            sleep(2)
            scrape.session.download_to(s, base_url.format(playerid), "input/player-{}.html".format(playerid))
        sleep(5)
	
def main():
    fetch_list = sys.argv[3:] if len(sys.argv) > 3 else range(5, 3535)
    download_all_players(fetch_list)


if __name__ == "__main__":
    main()
