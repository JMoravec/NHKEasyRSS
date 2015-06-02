from bs4 import BeautifulSoup
import datetime
import httplib2


def get_and_parse_page(link_to_page):
    h = httplib2.Http()
    (resp_headers, content) = h.request(link_to_page, "GET")
    soup = BeautifulSoup(content)
    title = soup.find(id="newstitle").find('h2')
    article = soup.find(id="newsarticle")
    img_tag = soup.find(id="mainimg").img
    return title.contents, article.contents, img_tag['src']


def create_new_entry(title_contents, article_contents, link, img_link=''):
    soup = BeautifulSoup("<entry></entry>")
    entry_tag = soup.entry
    id_tag = soup.new_tag('id')
    title_tag = soup.new_tag('title')
    updated_tag = soup.new_tag('updated')
    content_tag = soup.new_tag('content')
    link_tag = soup.new_tag('link')

    entry_tag.append(id_tag)
    entry_tag.append(title_tag)
    entry_tag.append(updated_tag)
    entry_tag.append(content_tag)
    entry_tag.append(link_tag)

    id_tag.string = link
    link_tag['href'] = link
    title_tag.contents = title_contents
    title_tag['type'] = 'xhtml'
    content_tag['type'] = 'xhtml'

    img_tag = soup.new_tag('img')
    img_tag['src'] = img_link
    article_contents.insert(0, img_tag)
    content_tag.contents = article_contents
    updated_tag.string = datetime.datetime.now().isoformat('T')
    return entry_tag
