#!/usr/bin/env python3
from bs4 import BeautifulSoup
import logging
import json
import sys
from os import listdir
import os.path

from match import parse
from importer.bbleague.defaults import BASEPATH

LOG = logging.getLogger(__package__)


def parse_match(filename):
    if (filename.startswith("match")):
        return parse.open_match(from_file(filename))
    return None


def process_matchdata(match, directory):
    matchdatafile = os.path.join(directory, "html/match/", "matchdata-{}.html".format(match["matchid"]))

    # print(match["matchid"])
    with open(matchdatafile, "rb") as fp:
        linje = fp.read().decode("latin-1")
        matchdata = parse.parse_matchdata(linje)
        match["away_coachid"] = matchdata["coach2"]
        match["home_coachid"] = matchdata["coach1"]

        return match
    return match


def process_match(directory, filename):
    LOG.debug("Process single match %s %s", directory, filename)
    matchid = filename[filename.find("match-") + 6:filename.rfind(".html")]
    match = parse.parse_match(matchid, from_file("{}/html/match/{}".format(directory, filename)))
    # print(match)
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
        if (filename.startswith("match-")):
            match = process_match(directory, filename)
            if match:
                matches.append(match)

    return matches


def from_files(directory):
    match_path = os.path.join(directory, "html/match/")
    LOG.debug("listing files in %s", directory)
    return process_matches(directory, listdir(match_path))


def create_json_cache(basepath = BASEPATH):
    LOG.debug("Creating json cache using %s", basepath)
    import json
    filepath = os.path.join(basepath, "json/match-all.json")
    match_html_directory = os.path.join(basepath, "html/match/")
    matches = from_files(basepath)

    LOG.debug("Dump %s matches into %s", len(matches), filepath)
    if len(matches) == 0:
        LOG.warning("No matches found in %s", basepath)
    with open(filepath, "w") as fp:
        json.dump(matches, fp, indent=4)

    return matches


def create_cache(directory=BASEPATH, filename="json/match-all.json"):
    import os.path
    match_all_filename = os.path.join(directory, filename)
    match_html_directory = os.path.join(directory, "html/match")

    if not os.path.isfile(match_all_filename):
        LOG.debug("%s does not exist", match_all_filename)
        return True
    LOG.debug("Found %s", match_all_filename)

    json_mtime = os.path.getmtime(match_all_filename)
    for checkfile in listdir(match_html_directory):
        LOG.debug("Checking %s", checkfile)
        if checkfile.startswith("match") and os.path.getmtime(os.path.join(directory,"html/match", checkfile)) > json_mtime:
            LOG.debug("Modified since %s", json_mtime)
            return True
    return False


def from_json(basepath = BASEPATH):
    LOG.debug("From json %s json/match-all.json", basepath)
    if create_cache(basepath, "json/match-all.json"):
        print("Creating cache")
        return create_json_cache(basepath)
    with open(basepath + "json/match-all.json") as fp:
        return json.load(fp)


def from_file(filename):
    LOG.debug("From file %s", filename)
    if not os.path.isfile(filename):
        LOG.warning("File %s does not exist", filename)
    matchid = filename[filename.find("match-") + 6:filename.rfind(".html")]
    LOG.debug("match id: %s", matchid)
    html = open(filename, "rb").read()
    soup = BeautifulSoup(html, "lxml")
    return soup


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    LOG.info("Parsing teamlist for coaches")

    # import parse
    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(process_match(sys.argv[1] if len(sys.argv) > 1 else BASEPATH, "match-{}.html".format(sys.argv[2])))


if __name__ == "__main__":
    main()
