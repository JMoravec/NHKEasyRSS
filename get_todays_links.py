import datetime
import json
import httplib2


def get_todays_links(link):
    links = []
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    h = httplib2.Http()
    (resp_headers, content) = h.request(link, 'get')
    try:
        all_data = json.loads(content.decode('utf-8-sig'))[0][today]
        for data in all_data:
            links.append(data['news_web_url'])

        return links
    except:
        print('No links yet for today')
        return []