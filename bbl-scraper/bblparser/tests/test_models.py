from bblparser.models import Link


def test_link_get_link_return_str():
    assert Link(href=None, onclick=None, text='Heading').get_link() is None

    onclick_link = "self.location.href='?p=rs&s=34';"
    assert 'the_base+?p=rs&s=34' == Link(href=None, onclick=onclick_link, text='Heading').get_link(base='the_base+')
    assert 'the_base+default.asp?p=tm&t=roy2' == Link(href='default.asp?p=tm&t=roy2', onclick=None, text='Heading').get_link(base='the_base+')
    assert 'the_base+this_link' == Link(href='this_link', onclick='not_this_link', text='not_this_text').get_link(base='the_base+')
