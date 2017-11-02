#!/usr/bin/env python
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

def list_coaches():
    return parse.load()

def find_uid_for_nick(coaches, nick):
    for the_coach in coaches.values():
        if the_coach["nick"] == nick:
            return the_coach["uid"]
    return None
    #return [key for key, value in coaches if value["nick"] == nick]

def main():
    import sys
    coaches = list_coaches()
    for coach in coaches:
        if len(sys.argv) < 2 or coach["nick"]==" ".join(sys.argv[1:]) or "{}".format(coach["uid"])==sys.argv[1]:
            print (coach)
    print("Total: {}".format(len(coaches)))

if __name__ == "__main__":
    main()
