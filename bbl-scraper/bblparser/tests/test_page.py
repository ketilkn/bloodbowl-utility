import bblparser.page
from bblparser.models import Page, Link


def test_parse_return_page():
    r = bblparser.page.parse(html='<html>')

    assert isinstance(r, Page)


OUTER_HTML = """
<html>
    <body>
    <table style="border-top:0px solid #808080;border-bottom:0px solid #808080;border-left:0px solid #808080;border-right:0px solid #808080;background-color:transparent;background-image:url(gfx/bgfilframe.);background-repeat:repeat;background-position:left top" width="810" cellspacing="0" cellpadding="0" border="0" align="center">
        {}</table>
    </body>
</html>"""


#/html/body/table/tbody/tr[2]/td[1]/table/tbody/tr[3]/td
def test_parse_add_menu():
    inner = """<tr><td><table valign="top" width="100%" height="100%" cellspacing="0" cellpadding="0" border="0">
                    <tr><td></td></tr>
                    <tr><td class="menu" style="background-image:url(gfx/trans.gif)">### AnBBL Info ###</td></tr>
                    <tr>
    <td class="menu" style="background-image: url(&quot;gfx/trans.gif&quot;); cursor: pointer; color: rgb(0, 0, 0); background-color: transparent;" onmouseover="over(this);" onmouseout="out(this);" onclick="self.location.href='?p=rs&amp;s=34';">Semi Pro XVI</td>
</tr>
                    <tr><td class="menu" style="background-image: url(&quot;gfx/trans.gif&quot;); cursor: pointer; color: rgb(0, 0, 0); background-color: transparent;" onmouseover="over(this);" onmouseout="out(this);" onclick="self.location.href='?p=cp&amp;cpid=29';">### Statistics ###</td></tr>
                </td></tr></table>"""
    r = bblparser.page.parse(html=OUTER_HTML.format(inner))

    assert isinstance(r, Page)
    assert isinstance(r.menu, list)
    assert len(r.menu) == 3
    assert isinstance(r.menu[0], Link)
    assert r.menu[0].text == '### AnBBL Info ###'
    assert r.menu[0].onclick is None
    assert r.menu[1].text == 'Semi Pro XVI'
    assert r.menu[1].onclick == "self.location.href='?p=rs&s=34';"
    assert r.menu[2].text == '### Statistics ###'
    assert r.menu[2].onclick == "self.location.href='?p=cp&cpid=29';"

