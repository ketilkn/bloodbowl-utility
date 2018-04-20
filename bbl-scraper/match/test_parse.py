from bs4 import BeautifulSoup
import match.parse


def test_parse_match_works_for_unplayed():
    soup = BeautifulSoup(open("match/testdata/unplayed_match.html", "rb").read().decode("iso-8859-1"), "lxml")
    played_match = match.parse.parse_match(1161, soup)
    assert "approved" in played_match
    assert not played_match["approved"]

    assert "home_team" in played_match
    assert "away_team" in played_match

    assert played_match["home_teamid"] == "ank"
    assert played_match["home_team"] == "Ankerskogen Blodbaderklubb"
    assert played_match["away_teamid"] == "boer"


def test_parse_match_works_for_approved():
    soup = BeautifulSoup(open("match/testdata/match-1113.html", "rb").read().decode("iso-8859-1"), "lxml")
    played_match = match.parse.parse_match(1161, soup)

    assert "approved" in match

    assert played_match["home_teamid"] == "wam"
    assert played_match["home_team"] == "Wampire Counts von Norway"

    assert played_match["away_teamid"] == "und"
    assert played_match["away_team"] == "Underworld Overlords"


def test_return_false_on_invalid_match():
    soup = BeautifulSoup(open("match/testdata/invalid.html", "rb").read().decode("iso-8859-1"), "lxml")
    played_match = match.parse.parse_match(1043, soup)

    assert not played_match


def test_parse_return_foul_casualties():
    soup = BeautifulSoup(open("match/testdata/match-1190.html", "rb").read().decode("iso-8859-1"), "lxml")
    casualties = match.parse.find_casualties(soup)

    assert "home_cas_foul" in casualties
    assert "away_cas_foul" in casualties



