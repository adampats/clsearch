#!/usr/bin/env python

import logging
import feedparser
from urlparse import urlparse
from os.path import splitext, basename

from IPython import embed
# embed()

### Default Parameters
defaults = {
    'all_cities': False,
    'all_state': None,
    'city': 'seattle',
    'search': 'cta?query=audi+s4&srchType=T&auto_paint=2'
}

### Script
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# for flattening nested lists of lists
flatten = lambda l: [item for sublist in l for item in sublist]

def handler(event, context):
    logger.info("%s - %s", event, context)
    cl = {}
    search_scope = []

    for key in defaults.keys():
        try:
            event[key]
        except KeyError, NameError:
            cl[key] = defaults[key]
        else:
            cl[key] = event[key]

    # Determine what cities to search
    if cl['city']:
        search_scope.append( [cl['city']] )
    if cl['all_state']:
        search_scope.append( Locations.States[cl['all_state']] )
    if cl['all_cities']:
        for state in Locations.States.itervalues():
            search_scope.append( state )

    search_scope = flatten(search_scope)
    print search_scope

    # Fetch matches from cities specified in search_scope
    records = {}
    for city in search_scope:
        url = "https://" + city + ".craigslist.org/search/" + \
            cl['search'] + "&format=rss"

        data = feedparser.parse(url)
        for entry in data.entries:
            new_record = {
                'id': splitext( basename( urlparse(entry['id']).path ))[0],
                'url': entry['id'],
                'title': entry['title']
            }
            records[new_record['id']] = new_record

    for k,v in records.iteritems():
        logger.info("-----")
        logger.info(k)
        logger.info(v['title'])
        logger.info(v['url'])


### Helper Classes

class Locations:
    States = {
        "oregon": [
            "bend",
            "corvallis",
            "eastoregon",
            "eugene",
            "klamath",
            "medford",
            "oregoncoast",
            "portland",
            "roseburg",
            "salem",
        ],
        "washington": [
            "bellingham",
            "kpr",
            "moseslake",
            "olympic",
            "pullman",
            "seattle",
            "skagit",
            "spokane",
            "wenatchee",
            "yakima"
        ]
    }
