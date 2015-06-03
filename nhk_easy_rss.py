from datetime import datetime
import sqlite3

import yaml
from bs4 import BeautifulSoup

from create_new_feed import create_new_feed
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


def create_db_date_entry(today_date):
    nhkconfig = yaml.load(open('config.yaml'))
    conn = sqlite3.connect(nhkconfig['db_file'])
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS nhk_date (id INTEGER PRIMARY KEY, date TEXT)''')
    conn.commit()
    c.execute('''CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY,
        link_url TEXT, date_id, FOREIGN KEY(date_id) REFERENCES nhk_date(id))''')
    conn.commit()

    today_date = (today_date,)
    c.execute('''SELECT COUNT(*) FROM nhk_date WHERE date = ?''', today_date)
    count = c.fetchone()[0]
    if count == 0:
        c.execute('''INSERT INTO nhk_date (date) VALUES (?)''', today_date)
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False


def create_db_link_entry(url_link, today_date):
    nhkconfig = yaml.load(open('config.yaml'))
    conn = sqlite3.connect(nhkconfig['db_file'])
    c = conn.cursor()
    c.execute('''SELECT id FROM nhk_date WHERE date = ?''', (today_date,))
    date_id = c.fetchone()[0]
    c.execute('''SELECT COUNT(*) FROM links WHERE date_id = ? AND link_url = ?''', (int(date_id), url_link))
    count = c.fetchone()[0]
    if count == 0:
        c.execute('''INSERT INTO links (date_id, link_url) VALUES (?,?)''', (date_id, url_link))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False


if __name__ == '__main__':
    config = yaml.load(open('config.yaml'))
    create_new_feed()
    today = datetime.now().strftime('%Y-%m-%d')
    if create_db_date_entry(today):
        links = get_todays_links(config['nhk_json'], today)
        if links:
            for link in links:
                if create_db_link_entry(link, today):
                    link_title, link_article, link_img = get_and_parse_page(link)
                    link_new_entry = create_new_entry(link_title, link_article, link_img)
                    add_new_entry_to_feed(link_new_entry)
