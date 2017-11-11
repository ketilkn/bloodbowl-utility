#!/usr/bin/env python3
from bs4 import BeautifulSoup
from unicodedata import normalize
import datetime
import dateutil.parser as parser
import re
#import team 
import sys
from os import listdir
import os.path

from match import parse

def parse_match(filename):
    if(filename.startswith("match")):
        return parse.open_match(from_file(filename))
    return None

def process_matchdata(match, directory):
    matchdatafile = os.path.join(directory, "matchdata-{}.html".format(match["matchid"]))

    #print(match["matchid"])
    with open(matchdatafile, "rb") as fp:
        linje = fp.read().decode("latin-1")
        matchdata = parse.parse_matchdata(linje)
        match["away"]["coachid"] = matchdata["coach2"]
        match["home"]["coachid"] = matchdata["coach1"]

        return match
    return match

def process_match(directory, filename):
    matchid = filename[filename.find("match-")+6:filename.rfind(".html")]
    match = parse.parse_match(matchid, from_file("{}/{}".format(directory ,filename)))
    #print(match)
    if match:
        if "date" in match and match["date"]:
            match = process_matchdata(match, directory)
            return match
        else:
            print("No date in file {}".format(filename), file=sys.stderr)
            return None
    return None

def process_matches(directory, files):
    matches = []
    for filename in files:
        if(filename.startswith("match-")):
            match = process_match(directory, filename)
            if match:
                matches.append(match)

    return matches

def from_files(directory):
    return process_matches(directory, listdir(directory))    

def create_json_cache(directory):
    import json
    
    matches = from_files(directory)
    with open("input/json/match-all.json", "w") as fp:
        json.dump(matches, fp, indent=4)

    return matches 

def create_cache(directory="input", filename="input/json/match-all.json"):
    import os.path
    if not os.path.isfile(filename):
        return True
    json_mtime = os.path.getmtime(filename)
    for checkfile in listdir(directory):
        if checkfile.startswith("match") and os.path.getmtime(os.path.join(directory, checkfile)) > json_mtime:
            return True
    return False

def from_json():
    import json
    import os.path
    if create_cache("input/", "input/json/match-all.json"):
        print("Creating cache")
        return create_json_cache("input/html/match/")
    with open("input/json/match-all.json") as fp:
        return json.load(fp)

def from_file(filename):
        matchid = filename[filename.find("match-")+6:filename.rfind(".html")]
        html = open(filename, "rb").read()
        soup = BeautifulSoup(html, "lxml")
        return soup

def main():
        #import parse
        import pprint
        pp = pprint.PrettyPrinter(indent=4)

        pp.pprint(process_match("input/html/match/", "match-{}.html".format(sys.argv[1])))

if __name__ == "__main__":
    main()
