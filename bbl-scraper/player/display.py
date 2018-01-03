#!/usr/env python3
import sys
import player.player
from .load import load_all


def plformat(p):
    return "{:>4} {:>32} {:>18} t:{:<4} c:{:>2} p:{:>3} i:{:>2} m:{:>2} g:{:>2} *:{:>3} {} {}".format(
        p["playerid"],
        p["playername"],
        p["position"][:18],
        p["team"] if p["team"] else "0000",
        p["spp"]["casualty"],
        p["spp"]["completion"],
        p["spp"]["interception"],
        p["spp"]["mvp"],
        p["spp"]["td"],
        p["spp"]["total"],
        ",".join(p["upgrade"]["normal"]+p["upgrade"]["extra"]+p["status"]["injury"]),
        p["status"]["active"]["reason"])


def plprint(p, end='\n'):
    print(plformat(p) , end=end)

def psa(players):
    for p in players:
        plprint(p)

def main():
    players = list(load_all())

    psa(sorted(players, key=lambda p: int(p["spp"]["total"]) if p["spp"]["total"] else 0))


if __name__=="__main__":
    main()
