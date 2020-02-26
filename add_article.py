import json
import time

import bs4
import feedparser
import markdown
import requests
import schedule
import tomd
from dateutil.parser import parse
from listparser import urllib

ARTICLE_URL = 'http://127.0.0.1:5000/api/v1.0/articles'
FEED_URL = 'http://127.0.0.1:5000/api/v1.0/channels'


def parse_rss_feed(item):
    print(item)
    json_item = {'channel_url': item['url'], 'channel_uuid': item['uuid'], 'channel_title': item['title']}
    print(item['url'])
    info = feedparser.parse(item['url'])
    data_list = info['entries']
    print(len(data_list))
    if data_list:
        for data in data_list:
            value = data['content'][0]['value']
            value = tomd.Tomd(value).markdown
            json_item['content'] = markdown.markdown(value)
            json_item['url'] = data['link']
            json_item['updated'] = time.strftime('%Y-%m-%d %H:%M:%S', data['updated_parsed'])
            json_item['summary'] = data['summary']
            json_item['title'] = data['title']
            res = requests.post(ARTICLE_URL, json.dumps(json_item))
            print(res.content)
    else:
        data = urllib.request.urlopen(item['url']).read()
        soup = bs4.BeautifulSoup(data, "html.parser")
        ch = soup.findAll('channel')[0]
        a = ch.findAll('item')
        print('len(a)', len(a))
        for i in a:
            json_item['content'] = i('content:encoded')[0].extract().text
            json_item['url'] = i.guid.text
            json_item['updated'] = parse(i.pubdate.text, fuzzy=True).strftime("%Y-%m-%d %H:%M:%S")
            json_item['summary'] = i.description.text
            json_item['title'] = i.title.text
            res = requests.post(ARTICLE_URL, json.dumps(json_item))
            print(res.content)


def job():
    res = json.loads(requests.get(FEED_URL).content)['data']
    for item in res:
        try:
            parse_rss_feed(item)
        except Exception as e:
            print(e)
            pass


def run():
    schedule.every(10).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    job()
