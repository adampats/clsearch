#!/usr/bin/env python

import logging
import feedparser
from urlparse import urlparse
from os.path import splitext, basename
from IPython import embed
# embed()

### Parameters
location = 'seattle'
national_search = False
default_search = 'cta?query=audi+s4&srchType=T&auto_paint=2'

### Script
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info("%s - %s", event, context)

    try:
        event['search_string']
    except NameError:
        search = default_search
    else:
        search = event['search_string']

    url = "https://" + location + ".craigslist.org/search/" + \
        search + "&format=rss"

    data = feedparser.parse(url)

    records = []
    for entry in data.entries:
        records.append({
            'id': splitext( basename( urlparse(entry['id']).path ))[0],
            'url': entry['id'],
            'title': entry['title']
        })

    for r in records:
        logger.info("-----")
        logger.info("%s", r['id'])
        logger.info("%s", r['title'])
        logger.info("%s", r['url'])
