#!/usr/bin/env python
"""  default functionality for bbleague importer """
import sys
import logging

import importer.bbleague.update

LOG = logging.getLogger(__package__)


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    section = "test" if len(sys.argv) < 2 else sys.argv[1]
    config = importer.bbleague.update.load_config(section)
    importer.bbleague.update.import_bloodbowlleague(config)


if __name__ == "__main__":
    main()