# with changes, from https://gist.github.com/cleverdevil/a8215850420493c1ee06364161e281c0
from xml.etree import ElementTree
from datetime import datetime
from dateutil.tz import UTC
from dateutil.parser import parse as parse_dt

import conf
import re
import sys

# import requests
# import pickle
import os.path
import json

# fetch the latest detailed OPML export from Overcast
# cache the last OPML file
try:
    with open("/Users/dk/Downloads/overcast.opml", "r") as reader:
        response = reader.read()
except:
    print("Unable to cache OPML file.")

# parse the OPML
tree = ElementTree.fromstring(response)

# find all podcasts and their episodes
podcasts = tree.findall(".//*[@type='rss']")

# look for recently played episodes
# now = datetime.utcnow().astimezone(UTC)
print("    Podcasts")
for podcast in podcasts:
    print(f"Podcast {podcast.attrib['title']}")
    for episode in list(podcast):
        played = episode.attrib.get("played", "0") == "1"
        if played:
            mark = "x"
        else:
            mark = "o"
        title = episode.attrib["title"]
        progress = episode.attrib.get("progress")
        results = re.findall('meta name="og:description" content="(.*)"', response)
        summary = (
            title
        )  # initialize with title, substitute with results below, if available
        if len(results) == 1 and len(results[0]):
            summary = results[0]
        print(f"    {mark}   {title}")
