#!/usr/bin/env python
"""  Test tournament pairing """
import sys
import pytest
import logging
from tournament.pairing import swiss_pairing, pairing, match_played, find_opponent

LOG = logging.getLogger(__package__)

STANDINGS = [{'name': 'test team 2', 'position': 1, 'teamid': 'tes2'},
{'name': 'Test team K', 'position': 2, 'teamid': 'tes3'},
{'name': 'Dust Bunnies', 'position': 3, 'teamid': 'dus'},
{'name': 'Demolition men', 'position': 4, 'teamid': 'dem'},
{'name': 'The Dwarf Giants', 'position': 5, 'teamid': 'dwa'},
{'name': 'Amazons', 'position': 6, 'teamid': 'les'},
{'name': 'Reikland Reavers', 'position': 7, 'teamid': 'rei'},
{'name': 'Underworld Creepers', 'position': 8, 'teamid': 'und'},
{'name': 'Chaos All-stars', 'position': 9, 'teamid': 'cha'},
{'name': 'Ogreheim Manglers', 'position': 10, 'teamid': 'ogr'}]


def test_swiss_pairing_return_list():
    assert type(swiss_pairing([], [])) == list


def test_swiss_pairing_after_one_round():
    matches = swiss_pairing(STANDINGS, [])
    print(matches)
    paired = swiss_pairing(STANDINGS, matches)
    print("========")
    assert len(paired) == 5, "Expected 6 matches"

    assert paired[0]["home_team"]["teamid"] == "tes2"
    assert paired[0]["away_team"]["teamid"] == "dus"

    assert paired[1]["home_team"]["teamid"] == "tes3"
    assert paired[1]["away_team"]["teamid"] == "dem"

    assert paired[2]["home_team"]["teamid"] == "dwa"
    assert paired[2]["away_team"]["teamid"] == "rei"

    #assert matches[4]["away_team"]["teamid"] == "les"
    #assert matches[3]["away_team"]["teamid"] == "cha"

    #assert matches[3]["home_team"]["teamid"] == "und"
    #assert matches[4]["away_team"]["teamid"] == "ogr"


def test_swiss_pairing_return_matches():
    matches = swiss_pairing(STANDINGS, [])
    assert type(matches) == list
    assert len(matches) == 5, "Expected 6 matches"
    assert matches[0]["home_team"]["teamid"] == "tes2"
    assert matches[0]["away_team"]["teamid"] == "tes3"
    assert matches[1]["home_team"]["teamid"] == "dus"
    assert matches[1]["away_team"]["teamid"] == "dem"
    assert matches[2]["home_team"]["teamid"] == "dwa"
    assert matches[2]["away_team"]["teamid"] == "les"
    assert matches[3]["home_team"]["teamid"] == "rei"
    assert matches[3]["away_team"]["teamid"] == "und"
    assert matches[4]["home_team"]["teamid"] == "cha"
    assert matches[4]["away_team"]["teamid"] == "ogr"


def test_pairing_require_standings():
    with pytest.raises(ValueError):
        pairing([], [], "swiss")


def test_match_played():
    matches = [{'away_team': {'teamid': 'tes3', 'name': 'Test team K', 'position': 2},
                'home_team': {'teamid': 'tes2', 'name': 'test team 2', 'position': 1}}]

    assert match_played({'teamid': 'tes2', 'name': 'test team 2', 'position': 1},
                        {'teamid': 'tes3', 'name': 'Test team K', 'position': 2},
                        matches)


def test_find_opponent():
    matches = swiss_pairing(STANDINGS, [])

    assert find_opponent({'teamid': 'tes2', 'name': 'test team 2', 'position': 1},
                         STANDINGS[1:],
                         matches) == {'name': 'Dust Bunnies', 'position': 3, 'teamid': 'dus'}


