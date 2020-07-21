import io
import logging
import pathlib
import typing
import sys

import bs4

from bblparser.models import Page, Link
import bblparser.load

LOG = logging.getLogger(__name__)


def _parse_link(el: bs4.element.Tag) -> Link:
    onclick = el.get('onclick') if el.has_attr('onclick') else None
    return Link(text=el.text, href=None, onclick=onclick)


def parse_menu(soup: bs4.BeautifulSoup) -> typing.List[bblparser.models.Link]:
    return [_parse_link(link) for link in soup.select('td.menu')]


def parse(html: str) -> bblparser.models.Page:
    soup = bs4.BeautifulSoup(html, 'lxml')
    if soup:
        return Page(menu=parse_menu(soup=soup),
                                 latest_matches=None,
                                 latest_bulletins=None)
    return None


def main():
    import argparse
    encoding = 'utf_8' if '--utf-8' in sys.argv else 'latin-1'
    print(encoding)
    arg_p = argparse.ArgumentParser()
    arg_p.add_argument('documents', nargs='*', type=str, default=[sys.stdin], help="HTML code to parse")
    arg_p.add_argument('--pprint', type=int, default=40, help="Pretty print parser result")
    arg_p.add_argument('--utf-8', action='store_true', help="Use UTF-8 encoding. default is latin-1")
    arg_p.add_argument('--json', action='store_true', help="JSON print parser result")

    arguments = arg_p.parse_args()
    result = next(bblparser.load.load_documents(arguments.documents))
    if arguments.pprint > 0 or arguments.pprint == -1:
        import pprint
        if arguments.pprint > 0:
            pprint.pprint(result[:arguments.pprint])
        else:
            pprint.pprint(result)
    return result, arguments


r = None
if __name__ == '__main__':
    r = main()
