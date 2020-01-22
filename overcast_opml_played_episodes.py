# with changes, from https://gist.github.com/cleverdevil/a8215850420493c1ee06364161e281c0
from xml.etree import ElementTree
from datetime import datetime
from dateutil.tz import UTC
from dateutil.parser import parse as parse_dt

import conf
import re
import sys
import requests
import pickle
import os.path
import json


# fetch the latest detailed OPML export from Overcast
# cache the last OPML file
try:
    with open('/Users/dk/Downloads/overcast.opml', 'r') as reader:
        response = reader.read()
except:
    print('Unable to cache OPML file.')


# parse the OPML
tree = ElementTree.fromstring(response)

# find all podcasts and their episodes
podcasts = tree.findall(".//*[@type='rss']")

# look for recently played episodes
now = datetime.utcnow().astimezone(UTC)
for podcast in podcasts:
    pod_title = podcast.attrib['title']
    for episode in list(podcast):
        # skip unplayed episodes
        played = episode.attrib.get('played', '0') == '1'
        if not played:
            continue

        # skip episodes played over 5 days ago
        user_activity_date_raw = episode.attrib.get('userUpdatedDate')
        user_activity_date = parse_dt(user_activity_date_raw)
        recency = now - user_activity_date
        if recency.days > 5:
            continue

        # parse out the remaining details we care about
        title = episode.attrib['title']
        published = parse_dt(episode.attrib['pubDate'])
        url = episode.attrib['url']
        overcast_url = episode.attrib['overcastUrl']
        overcast_id = episode.attrib['overcastId']
        progress = episode.attrib.get('progress')

        # fetch the episode summary
        results = re.findall('meta name="og:description" content="(.*)"', response)
        summary = title
        if len(results) == 1 and len(results[0]):
            summary = results[0]

        print('Played episode of ', pod_title)
        print('    ->', title)
        print('    ->', summary)
        # print('    ->', artwork_url)
        print('    ->', url)
        print('    ->', overcast_url)
        print('    ->', user_activity_date_raw)

        # build payload
        data = {
            'title': title,
            'summary': summary,
            'type': 'podcast',
            'author': pod_title,
            'link': overcast_url,
            'listenDateTime': user_activity_date_raw
        }


        print(json.dumps(data))

#        if response.status_code in (200, 201, 202):
#            open(footprint, 'w').write(json.dumps(data))
#            print('Successfully published!')
#            print(response.headers)
#        else:
#            print('Failed to publish!')
##            print(response)
