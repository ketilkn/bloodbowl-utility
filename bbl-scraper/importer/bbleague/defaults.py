#!/usr/bin/env python
"""  Default values for bloodbowlleague importerer """
import logging

LOG = logging.getLogger(__package__)
BASEPATH = "input/anarchy.bloodbowlleague.com/"


def main():
    log_format = "[%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s ] %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)


if __name__ == "__main__":
    main()