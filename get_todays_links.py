import json

import httplib2
import yaml


def get_todays_links(link, today):
    config = yaml.load(open('config.yaml'))
    links = []

    h = httplib2.Http()
    (resp_headers, content) = h.request(link, 'get')
    try:
        all_data = json.loads(content.decode('utf-8-sig'))[0][today]
        for data in all_data:
            links.append(config['nhk_root'] + data['news_id'] + '/'
                         + data['news_id'] + '.html')

        return links
    except Exception as e:
        print(e)
        print('No links yet for today')
        return []