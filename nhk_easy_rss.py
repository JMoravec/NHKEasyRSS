import yaml
from create_new_feed import create_new_feed
from bs4 import BeautifulSoup
from get_todays_links import get_todays_links
from nhk_page import get_and_parse_page
from nhk_page import create_new_entry


def add_new_entry_to_feed(new_entry):
    config = yaml.load(open('config.yaml'))

    feed_file = open(config['feed_location'], 'r')
    soup = BeautifulSoup(feed_file)
    feed_file.close()

    soup.feed.append(new_entry)
    feed_file = open(config['feed_location'], 'w')
    print(config['feed_xml'] + soup.feed.prettify(), file=feed_file)
    feed_file.close()

"""create_new_feed()
test_link = 'http://www3.nhk.or.jp/news/easy/k10010045751000/k10010045751000.html'
test_title, test_article, img_link = get_and_parse_page(test_link)
test_new_entry = create_new_entry(test_title, test_article, test_link, img_link)
add_new_entry_to_feed(test_new_entry)
"""

config = yaml.load(open('config.yaml'))
links = get_todays_links(config['nhk_json'])
create_new_feed()
for link in links:
    #link.replace("'", "")
    link_title, link_article, link_img = get_and_parse_page(link)
    link_new_entry = create_new_entry(link_title, link_article, link_img)
    add_new_entry_to_feed(link_new_entry)
