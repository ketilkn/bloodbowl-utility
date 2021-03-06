#!/usr/bin/env python
"""  default functionality for bbleague importer """
import sys
import logging
import argparse

import importer.bbleague.update

LOG = logging.getLogger(__package__)


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG if "--debug" in sys.argv else logging.INFO, format=log_format)

    argparser = argparse.ArgumentParser()
    argparser.add_argument("function", choices=["update", "initialize", "collate"], help="update")
    argparser.add_argument("site", help="[Site] from bbl-scrape.ini")
    argparser.add_argument("--debug", action="store_true", help="")
    args = argparser.parse_args()

    section = "test" if len(sys.argv) < 2 else sys.argv[1]
    config = importer.bbleague.update.load_config(args.site)
    if args.function == "update":
        importer.bbleague.update.import_bbleague(config)
    else:
        print("Nothing to do with {}".format(args.function))


if __name__ == "__main__":
    main()