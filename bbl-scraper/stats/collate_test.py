#!/usr/bin/python3
import pprint
import stats.collate
import sys
def pretty(value):
    pprint.pprint(value, indent=2)

def match_sans_coach(data):
    no_coachid = [match["matchid"] for match in data["game"].values() if match["away_coachid"] in ["-1", 0, -1, "0", None] or match["home_coachid"] in ["0","-1", 0, -1,  None]]
    print("{}\ncount: {}".format(sorted(no_coachid, key=lambda x: int(x)), len(no_coachid)))

def main():
    data = stats.collate.collate()
    print([[key, len(data[key])] for key in data.keys()])



if __name__ == "__main__":
    main()
