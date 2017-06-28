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
        for state in cl['all_state']:
            search_scope.append( Locations.States[state] )
    if cl['all_cities']:
        for state in Locations.States.itervalues():
            search_scope.append( state )

    search_scope = flatten(search_scope)
    logger.info("search scope: %s" % search_scope)

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

    if (records == {}):
        logger.info("Nothing found!")

    for k,v in records.iteritems():
        logger.info("-----")
        logger.info(k)
        logger.info(v['title'])
        logger.info(v['url'])


### Helper Classes

class Locations:
    States = {
        "Alabama": [
            "auburn", "bham", "dothan", "shoals", "gadsden", "huntsville",
            "mobile", "montgomery", "tuscaloosa"
        ],
        "Alaska": [
            "anchorage", "fairbanks", "kenai", "juneau"
        ],
        "Arizona": [
            "flagstaff", "mohave", "phoenix", "prescott", "showlow",
            "sierravista", "tucson", "yuma"
        ],
        "Arkansas": [
            "fayar", "fortsmith", "jonesboro", "littlerock", "texarkana"
        ],
        "California": [
            "bakersfield", "chico", "fresno", "goldcountry", "hanford",
            "humboldt", "imperial", "inlandempire", "losangeles", "mendocino",
            "merced", "modesto", "monterey", "orangecounty", "palmsprings",
            "redding", "sacramento", "sandiego", "sfbay", "slo", "santabarbara",
            "santamaria", "siskiyou", "stockton", "susanville", "ventura",
            "visalia", "yubasutter"
        ],
        "Colorado": [
            "boulder", "cosprings", "denver", "eastco", "fortcollins",
            "rockies", "pueblo", "westslope"
        ],
        "Connecticut": [
            "newlondon", "hartford", "newhaven", "nwct"
        ],
        "Delaware": [
            "delaware"
        ],
        "District of Columbia": [
            "washingtondc"
        ],
        "Florida": [
            "miami", "daytona", "keys", "fortlauderdale", "fortmyers",
            "gainesville", "cfl", "jacksonville", "lakeland", "miami",
            "lakecity", "ocala", "okaloosa", "orlando", "panamacity",
            "pensacola", "sarasota", "miami", "spacecoast", "staugustine",
            "tallahassee", "tampa", "treasure", "miami"
        ],
        "Georgia": [
            "albanyga", "athensga", "atlanta", "augusta", "brunswick",
            "columbusga", "macon", "nwga", "savannah", "statesboro", "valdosta"
        ],
        "Hawaii": [
            "honolulu"
        ],
        "Idaho": [
            "boise", "eastidaho", "lewiston", "twinfalls"
        ],
        "Illinois": [
            "bn", "chambana", "chicago", "decatur", "lasalle", "mattoon",
            "peoria", "rockford", "carbondale", "springfieldil", "quincy"
        ],
        "Indiana": [
            "bloomington", "evansville", "fortwayne", "indianapolis", "kokomo",
            "tippecanoe", "muncie", "richmondin", "southbend", "terrehaute"
        ],
        "Iowa": [
            "ames", "cedarrapids", "desmoines", "dubuque", "fortdodge",
            "iowacity", "masoncity", "quadcities", "siouxcity", "ottumwa",
            "waterloo"
        ],
        "Kansas": [
            "lawrence", "ksu", "nwks", "salina", "seks", "swks", "topeka",
            "wichita"
        ],
        "Kentucky": [
            "bgky", "eastky", "lexington", "louisville", "owensboro", "westky"
        ],
        "Louisiana": [
            "batonrouge", "cenla", "houma", "lafayette", "lakecharles",
            "monroe", "neworleans", "shreveport"
        ],
        "Maine": [
            "maine"
        ],
        "Maryland": [
            "annapolis", "baltimore", "easternshore", "frederick", "smd",
            "westmd"
        ],
        "Massachusetts": [
            "boston", "capecod", "southcoast", "westernmass", "worcester"
        ],
        "Michigan": [
            "annarbor", "battlecreek", "centralmich", "detroit", "flint",
            "grandrapids", "holland", "jxn", "kalamazoo", "lansing", "monroemi",
            "muskegon", "nmi", "porthuron", "saginaw", "swmi", "thumb", "up"
        ],
        "Minnesota": [
            "bemidji", "brainerd", "duluth", "mankato", "minneapolis", "rmn",
            "marshall", "stcloud"
        ],
        "Mississippi": [
            "gulfport", "hattiesburg", "jackson", "meridian", "northmiss",
            "natchez"
        ],
        "Missouri": [
            "columbiamo", "joplin", "kansascity", "kirksville", "loz", "semo",
            "springfield", "stjoseph", "stlouis"
        ],
        "Montana": [
            "billings", "bozeman", "butte", "greatfalls", "helena", "kalispell",
            "missoula", "montana"
        ],
        "Nebraska": [
            "grandisland", "lincoln", "northplatte", "omaha", "scottsbluff"
        ],
        "Nevada": [
            "elko", "lasvegas", "reno"
        ],
        "New Hampshire": [
            "nh"
        ],
        "New Jersey": [
            "cnj", "jerseyshore", "newjersey", "southjersey"
        ],
        "New Mexico": [
            "albuquerque", "clovis", "farmington", "lascruces", "roswell",
            "santafe"
        ],
        "New York": [
            "albany", "binghamton", "buffalo", "catskills", "chautauqua",
            "elmira", "fingerlakes", "glensfalls", "hudsonvalley", "ithaca",
            "longisland", "newyork", "oneonta", "plattsburgh", "potsdam",
            "rochester", "syracuse", "twintiers", "utica", "watertown"
        ],
        "North Carolina": [
            "asheville", "boone", "charlotte", "eastnc", "fayetteville",
            "greensboro", "hickory", "onslow", "outerbanks", "raleigh",
            "wilmington", "winstonsalem"
        ],
        "North Dakota": [
            "bismarck", "fargo", "grandforks", "nd"
        ],
        "Ohio": [
            "akroncanton", "ashtabula", "athensohio", "chillicothe",
            "cincinnati", "cleveland", "columbus", "dayton", "limaohio",
            "mansfield", "sandusky", "toledo", "tuscarawas", "youngstown",
            "zanesville"
        ],
        "Oklahoma": [
            "lawton", "enid", "oklahomacity", "stillwater", "tulsa"
        ],
        "Oregon": [
            "bend", "corvallis", "eastoregon", "eugene", "klamath", "medford",
            "oregoncoast", "portland", "roseburg", "salem"
        ],
        "Pennsylvania": [
            "altoona", "chambersburg", "erie", "harrisburg", "lancaster",
            "allentown", "meadville", "philadelphia", "pittsburgh", "poconos",
            "reading", "scranton", "pennstate", "williamsport", "york"
        ],
        "Rhode Island": [
            "providence"
        ],
        "South Carolina": [
            "charleston", "columbia", "florencesc", "greenville", "hiltonhead",
            "myrtlebeach"
        ],
        "South Dakota": [
            "nesd", "csd", "rapidcity", "siouxfalls", "sd"
        ],
        "Tennessee": [
            "chattanooga", "clarksville", "cookeville", "jacksontn",
            "knoxville", "memphis", "nashville", "tricities"
        ],
        "Texas": [
            "abilene", "amarillo", "austin", "beaumont", "brownsville",
            "collegestation", "corpuschristi", "dallas", "nacogdoches",
            "delrio", "elpaso", "galveston", "houston", "killeen", "laredo",
            "lubbock", "mcallen", "odessa", "sanangelo", "sanantonio",
            "sanmarcos", "bigbend", "texoma", "easttexas", "victoriatx", "waco",
            "wichitafalls"
        ],
        "Utah": [
            "logan", "ogden", "provo", "saltlakecity", "stgeorge"
        ],
        "Vermont": [
            "vermont"
        ],
        "Virginia": [
            "charlottesville", "danville", "fredericksburg", "norfolk",
            "harrisonburg", "lynchburg", "blacksburg", "richmond", "roanoke",
            "swva", "winchester"
        ],
        "Washington": [
            "bellingham", "kpr", "moseslake", "olympic", "pullman", "seattle",
            "skagit", "spokane", "wenatchee", "yakima"
        ],
        "West Virginia": [
            "charlestonwv", "martinsburg", "huntington", "morgantown",
            "wheeling", "parkersburg", "swv", "wv"
        ],
        "Wisconsin": [
            "appleton", "eauclaire", "greenbay", "janesville", "racine",
            "lacrosse", "madison", "milwaukee", "northernwi", "sheboygan",
            "wausau"
        ],
        "Wyoming": [
            "wyoming"
        ]
    }
