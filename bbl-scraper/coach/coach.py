#!/usr/bin/env python
import os
import time
import json
from coach import parse

def dict_coaches(use_key="nick"):
    coaches = list_coaches()
    result = {}
    for coach in coaches:
        result[coach[use_key]] = coach
        #result[coach["uid"]] = coach
    return result

def dict_coaches_by_uid():
    return dict_coaches("uid")

def load_from_json():
    data = open("input/json/coaches.json", "rb").read()
    return json.loads(data.decode())


def save_to_json(coaches):
    data = json.dumps(coaches)
    json_file = open("input/json/coaches.json", "wb")
    json_file.write(data.encode())
    json_file.close()
    

def list_coaches():
    if not os.path.isfile("input/json/coaches.json") or os.stat("input/json/coaches.json").st_mtime < os.stat("input/html/coach/coaches-8.html").st_mtime:
        coaches = parse.load()
        save_to_json(coaches)
        return coaches
    return load_from_json()

def find_uid_for_nick(coaches, nick):
    for the_coach in coaches.values():
        if the_coach["nick"] == nick:
            return the_coach["uid"]
    return None
    #return [key for key, value in coaches if value["nick"] == nick]

def main():
    import sys
    coaches = list_coaches()
    coaches = dict_coaches_by_uid()
    for coach in coaches.values():
        if len(sys.argv) < 2 or coach["nick"]==" ".join(sys.argv[1:]) or coach["nick"] in sys.argv[1:] or coach["uid"] in sys.argv[1:]:
            print (coach)
    print("Total: {}".format(len(coaches)))

if __name__ == "__main__":
    main()
