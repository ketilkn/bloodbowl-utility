#!/bin/env python3
import sys
import requests
from time import sleep
import scrape.session

coaches_url = "http://www.anarchy.bloodbowlleague.com/default.asp?p=co"
	
def download_coach_list():
    s = scrape.session.login("http://www.anarchy.bloodbowlleague.com/login.asp", username=sys.argv[1], password=sys.argv[2])
    scrape.session.download_to(s, coaches_url, "input/html/coach/coaches-8.html")
	
def main():
    download_coach_list()

if __name__ == "__main__":
    main()
