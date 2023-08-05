from inkprint import InkPrinter


def test_init_with_two_available_colors():
    inkp = InkPrinter(paper_color='r', ink_color='c')
    assert inkp.paper_color == 'red'
    assert inkp.ink_color == 'cyan'


def test_init_with_same_color():
    inkp = InkPrinter(paper_color='green', ink_color='green')
    assert inkp.ink_color != 'green'


def test_colorizer():
    inkp = InkPrinter(paper_color='k', ink_color='r')
    assert inkp.colorizer == '\x1b[0;31;40m'