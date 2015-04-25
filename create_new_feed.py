import datetime
import yaml
import os.path
from bs4 import BeautifulSoup


def create_new_feed():
    config = yaml.load(open('config.yaml'))
    if not os.path.isfile(config['feed_location']):
        # Create initial feed info
        soup = BeautifulSoup(
            """<feed xmlns="http://www.w3.org/2005/Atom"></feed>""")
        feed_tag = soup.feed

        # Create required tags and add them in the feed tag
        title_tag = soup.new_tag('title')
        id_tag = soup.new_tag('id')
        updated_tag = soup.new_tag('updated')
        feed_tag.append(title_tag)
        feed_tag.append(id_tag)
        feed_tag.append(updated_tag)

        # Put data into the new feeds
        title_tag.string = config['feed_title']
        id_tag.string = config['feed_id']
        updated_tag.string = datetime.datetime.now().isoformat('T')

        feed_file = open(config['feed_location'], 'w')
        print(config['feed_xml'], file=feed_file)
        print(feed_tag.prettify(), file=feed_file)
        feed_file.close()
