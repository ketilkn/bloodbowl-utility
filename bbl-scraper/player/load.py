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

def from_file(filename):
        plyerid = filename[filename.find("player-")+6:filename.rfind(".html")]
        html = open(filename, "rb").read()
        soup = BeautifulSoup(html, "html.parser")
        return soup

def main():
        #import parse
        import pprint
        pp = pprint.PrettyPrinter(indent=4)

        pp.pprint(process_match("input", "match-{}.html".format(sys.argv[1])))

if __name__ == "__main__":
    main()
