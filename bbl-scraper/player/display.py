#!/usr/env python3
import sys
import player.player
from .load import load_all

def plprint(p):
    print("{:>4} {:>32} {:>18} ca:{:>2} cl:{:>2} in:{:>2} mv:{:>2} td:{:>2} to:{:>3}".format(
        p["playerid"], p["playername"], p["position"], p["spp"]["casualty"], p["spp"]["completion"], p["spp"]["interception"], p["spp"]["mvp"], p["spp"]["td"], p["spp"]["total"]))

def psa(ps):
    for p in players:
        plprint(p)

def main():
    players = list(load_all())
    psa(players)


if __name__=="__main__":
    main()
