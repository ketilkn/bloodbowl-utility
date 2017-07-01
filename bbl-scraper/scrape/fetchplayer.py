#!/bin/env python3
import sys
import requests
from time import sleep
import scrape.login


base_url = "http://www.anarchy.bloodbowlleague.com/default.asp?p=pladm&pid={}"

def slettmeg():
    for playerid in range(1178, 3341):
	print(base_url.format(playerid))
	try:
		with urllib.request.urlopen(base_url.format(playerid)) as respons:
			html = respons.readlines()
			open("output/player-{}.html".format(playerid), "wb").writelines(html)
			print("wrote file")
	except HTTPError as e:
		html = e.readlines()
		open("output/player-{}.html".format(playerid), "wb").writelines(html)
		print("wrote 500 file")
		
	sleep(10)
	
	
def main():
    print(sys.argv)
    s = scrape.login.login(sys.argv[1], sys.argv[2])
    print(s.cookies)
    if len(sys.argv) == 2 and sys.argv[1].isnumeric():
        download_match(sys.argv[1])
    elif len(sys.argv) == 3:
        from_match = int(sys.argv[1])
        to_match = int(sys.argv[2]) + 1
        download_matches(from_match, to_match)
    else:
        print("#Fetch recent games")
        games = new_games()
        print(" {} recent game{} {}".format(len(games), "s" if len(games)!=1 else "",  games))
        for g in games:
            if not is_match_downloaded(g) or force_download():
                print("#Downloading game {}".format(g))
                download_match(g)
            else:
                print("#Game {} already downloaded use --force to reload".format(g))

if __name__ == "__main__":
    main()
