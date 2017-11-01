#!/bin/env python3
import sys
import requests
from time import sleep
import scrape.session

base_url = "http://www.anarchy.bloodbowlleague.com/default.asp?p=pl&pid={}"
admin_url = "http://www.anarchy.bloodbowlleague.com/default.asp?p=pladm&pid={}"
	
def download_all_players():
    s = scrape.session.login(sys.argv[1], sys.argv[2])
    for playerid in range(12, 3529):
        if scrape.session.download_to(s, admin_url.format(playerid), "input/admin-player-{}.html".format(playerid)):
            sleep(2)
            scrape.session.download_to(s, base_url.format(playerid), "input/player-{}.html".format(playerid))
        sleep(5)
	
def main():
    download_all_players()
    #s = scrape.session.login(sys.argv[1], sys.argv[2])
    #print(s.cookies)
    #scrape.session.download_to(s, base_url.format(2807), "input/admin-player-2807.html")


if __name__ == "__main__":
    main()
