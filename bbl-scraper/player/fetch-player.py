#!/bin/env python3
import urllib.request
from urllib.error import HTTPError
from time import sleep


base_url = "http://www.anarchy.bloodbowlleague.com/default.asp?p=pl&pid={}"

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
	
	
