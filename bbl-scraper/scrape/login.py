#!/usr/bin/env python3
import requests
import sys

def verify_session(session, response = None):
    #TODO check if session is logged in
    return response.status_code == 200

def login(username, password):
    s = requests.session()
    r = s.post("http://www.anarchy.bloodbowlleague.com/login.asp", data={"user":username, "pass":password})

    if verify_session(s,r):
        return s
    #FIXME Throw exception ? / return None?
    print("Could not verify session")
    sys.exit("Could not verify session")

def new_session():
    pass

def main():
    session=login(sys.argv[1], sys.argv[2])   
    print("{}".format(session.cookies))

if __name__ == "__main__":
    main()
