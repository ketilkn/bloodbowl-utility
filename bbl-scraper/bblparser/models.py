from dataclasses import dataclass
import typing


@dataclass
class Link:
    href: str
    onclick: str
    text: str

    def get_link(self, base='http://anarchy.bloodbowlleague.com/'):
        if self.href:
            return "{base}{href}".format(base=base, href=self.href)
        if self.onclick:
            onclick = self.onclick[self.onclick.find("'?")+1:self.onclick.rfind("';")]
            return "{base}{onclick}".format(base=base,
                                            onclick=onclick)
        return None

    def is_link(self):
        return self.href or self.onclick

@dataclass
class Page:
    menu: typing.List[Link]
    latest_matches: typing.List[typing.Dict]
    latest_bulletins: typing.List[typing.Dict]


