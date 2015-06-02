import sqlite3
import yaml
from create_new_feed import create_new_feed
from bs4 import BeautifulSoup
from get_todays_links import get_todays_links
from nhk_page import get_and_parse_page
from nhk_page import create_new_entry

def add_new_entry_to_feed(new_entry):
    nhkconfig = yaml.load(open('config.yaml'))

    feed_file = open(nhkconfig['feed_location'], 'r')
    soup = BeautifulSoup(feed_file)
    feed_file.close()

    soup.feed.append(new_entry)
    feed_file = open(nhkconfig['feed_location'], 'w')
    print(nhkconfig['feed_xml'] + soup.feed.prettify(), file=feed_file)
    feed_file.close()


def create_db():
    nhkconfig = yaml.load(open('config.yaml'))
    conn = sqlite3.connect(nhkconfig['db_file'])
    c = conn.cursor()
    c.execute('''CREATE TABLE nhk_date
             (date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


if __name__ == '__main__':
    config = yaml.load(open('config.yaml'))
    create_new_feed()
    create_db()
    links = get_todays_links(config['nhk_json'])
    if links:
        for link in links:
            link_title, link_article, link_img = get_and_parse_page(link)
            link_new_entry = create_new_entry(link_title, link_article, link_img)
            add_new_entry_to_feed(link_new_entry)
