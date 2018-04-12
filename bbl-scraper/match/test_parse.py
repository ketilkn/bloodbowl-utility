from bs4 import BeautifulSoup
from match.parse import parse_match


def test_parse_match_works_for_unplayed():
    soup = BeautifulSoup(open("match/testdata/unplayed_match.html", "rb").read().decode("iso-8859-1"), "lxml")
    match = parse_match(1161, soup)
    assert "approved" in match
    assert not match["approved"]

    assert "home_team" in match
    assert "away_team" in match

    assert match["home_teamid"] == "ank"
    assert match["home_team"] == "Ankerskogen Blodbaderklubb"
    assert match["away_teamid"] == "boer"


def test_parse_match_works_for_approved():
    soup = BeautifulSoup(open("match/testdata/match-1113.html", "rb").read().decode("iso-8859-1"), "lxml")
    match = parse_match(1161, soup)

    assert "approved" in match

    assert match["home_teamid"] == "wam"
    assert match["home_team"] == "Wampire Counts von Norway"

    assert match["away_teamid"] == "und"
    assert match["away_team"] == "Underworld Overlords"


def test_return_false_on_invalid_match():
    soup = BeautifulSoup(open("match/testdata/invalid.html", "rb").read().decode("iso-8859-1"), "lxml")
    match = parse_match(1043, soup)

    assert not match




