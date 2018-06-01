#!/usr/bin/env python3
import requests
import sys





def download_to(session, url, target):
    response = session.get(url)
    if not response.history or response.status_code==200: 
        html = response.text
        try:
            open(target, "w").write(html)
            print(" Wrote {} to {}".format(url, target))
            return True
        except OSError:
            print(" Failed writing {} to {}".format(url, target))
    else:
        print(" Server error {} for {}".format(response.status_code, url))
    return False

def verify_session(session, response = None):
    #TODO check if session is logged in
    return response.status_code == 200

def login(url, username, password):
    s = requests.session()
    r = s.post(url, data={"user":username, "pass":password})

    if verify_session(s,r):
        return s
    #FIXME Throw exception ? / return None?
    print("Could not verify session")
    sys.exit("Could not verify session")

def new_session():
    return requests.session()

def main():
    session=login("http://www.anarchy.bloodbowlleague.com/login.asp", sys.argv[1], sys.argv[2])
    print("{}".format(session.cookies))

if __name__ == "__main__":
    main()
