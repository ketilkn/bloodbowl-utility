#!/usr/bin/env python
import sys
import os.path
import logging
from bs4 import BeautifulSoup
from unicodedata import normalize
import datetime
from importer.bbleague.defaults import BASEPATH

#import dateutil.parser as parser
NEVER_LOGGED_IN = "2000-01-01T00:00:01"

LOG = logging.getLogger(__package__)


def find_rows(soup):
    coaches = []
    rows = soup.find_all("tr")
    LOG.debug("Found %s rows", len(rows))
    for row in rows:
        if row.has_attr("height") and row['height'] == "27":
            coaches.append(row)

    return coaches
def parse_email(row):
    found = row.find_all("a")
    for a in found:
        if a.has_attr("href") and a["href"].startswith("mailto"):
            return a.text
    return "Found no email"
def parse_nick(row):
    found = row.find_all("td")
    for td in found:
        if td.has_attr("style") and td["style"]=="border-top:1px solid #808080;color:#203040":
            return td.find("b").text
    return "Found no nick"
def parse_uid(row):
    found = row.select("div.b1")
    for div in found:
        if div.has_attr("onclick"):
            onclick = div["onclick"]
            return onclick.split("&")[1][4:]

def parse_naf(row):
    found = row.find_all("div")
    for div in found:
        if div.text.startswith("NAF#:"):
            return div.text[6:]
def parse_role(row):
    return row.select('td[align="center"]')[1].text

def parse_phone(row):
    return row.select('td[align="center"]')[2].contents[0]

def parse_location(row):
    column  = row.select('td[align="center"]')[2].contents
    return column[2] if len(column) > 2 else "Old World" 

def parse_date(row):
    style_search="border-top:1px solid #808080;color:#404040;padding-top:3px;padding-bottom:1px"
    found = row.find_all("td")
    for td in found:
        if td.has_attr("style") and td["style"]==style_search:
            text = td.text.split("\xa0")[0]
            if text == "never logged in":
                return NEVER_LOGGED_IN
            clock = "00:00:00"
            year = "{}".format(datetime.datetime.now().year)
                
            if text.find("-")>0:
                clock = text.split("-")[1].strip()
                text = text.split("-")[0]
            if len(text.split("/")) == 3:
                year = text.split("/")[2]
                    
            return "{}-{}-{}T{}".format(year, text.split("/")[1].strip().zfill(2), text.split("/")[0].strip().zfill(2), clock)
    return "Found no date"
def parse_coach_row(row):
    coach = {'nick': parse_nick(row), 
            'email': parse_email(row),
            'naf': parse_naf(row),
            'role': parse_role(row),
            'phone': parse_phone(row),
            'location': parse_location(row),
            'login': parse_date(row),
            'loggedin': False,
            'uid': parse_uid(row)}
    
    if(coach["login"] != NEVER_LOGGED_IN):
        coach["loggedin"] = True
    parse_uid(row)
    return coach

def parse_rows(rows_of_coaches):
    coaches = []
    for row in rows_of_coaches:
        coaches.append(parse_coach_row(row))
    return coaches

def data_exists(basepath = BASEPATH):
    return os.path.isfile(basepath + "html/coach/coaches-8.html")


def load(basepath = BASEPATH):
    filepath = basepath + "html/coach/coaches-8.html"
    LOG.debug("Opening file %s", filepath)
    LOG.debug("exists: %s", os.path.isfile(filepath))
    html = open(filepath, "r").read()
    soup = BeautifulSoup(normalize("NFC", html), "lxml")
    print(soup)
    coaches = parse_rows(find_rows(soup))
    return coaches

def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    basepath = sys.argv[1] if len(sys.argv) > 1 else BASEPATH
    coaches = load(basepath)
    for coach in coaches:
        print(coach)
    print("Total: {}".format(len(coaches)))

if __name__ == "__main__":
    main()
