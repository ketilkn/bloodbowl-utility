#!/usr/bin/env python3
import sys
from importer import bbleague


if __name__ == '__main__':
    host = "www.anarchy.bloodbowlleague.com"
    username = sys.argv[1]
    password = sys.argv[2]
    bbleague.import_bloodbowlleague(host, username, password)
    #all_data.export_all_data()
