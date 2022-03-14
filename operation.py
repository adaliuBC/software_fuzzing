
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')

def operation_parser(data):
    from html.parser import HTMLParser
    parser = HTMLParser()
    parser.feed(data)
    parser = HTMLParser(convert_charrefs = True)
    parser.feed(data)


def operationWithSoup(data, parser):
    import bs4
    from bs4 import BeautifulSoup, CData, UnicodeDammit
    soup = BeautifulSoup(data, parser)
    soup.prettify()
    title = soup.title
    a = soup.a
    a = soup.find_all('a')
    link3 = soup.find(id = "link3")
    text = soup.get_text()

    tag = soup.a
    if tag != None:
        tag.name
        tag.name = "helloworld"
        for k, v in tag.attrs.items():
            del tag[k]
            tag[k] = ['180', 'conts']

    if tag.string:
        tag.string.replace_with("The roads goes ever on and on...")
    comment = soup.b.string
    cdata = CData("A CDATA block")
    if comment:  comment.replace_with(cdata)
    posstr = soup.string
    tag.find_next_siblings()
    tag.find_next_sibling()
    tag.find_previous_siblings()
    tag.find_previous_sibling()
    tag.find_previous()
    tag.find_all_previous()
    cont = soup.contents
    child = soup.children
    str = soup.string
    for str in soup.stripped_strings:
        pass
    soup.find_all(has_class_but_no_id)
    soup.find_all(a = "annatar")
    soup.find_all(string = "hello", limit = 3)
    soup.select("a")

def operation_bs4(data):
    import bs4
    from bs4 import BeautifulSoup, CData, UnicodeDammit
    pos = UnicodeDammit(data)
    operationWithSoup(data, "html.parser")
    operationWithSoup(data, "lxml")
    operationWithSoup(data, "html5lib")