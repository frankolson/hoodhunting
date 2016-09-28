#
# File to store functions related to filtering
#
from math import radians, cos, sin, asin, sqrt
import settings

def coord_distance(p1, p2):
    p1_lat, p1_lon, p2_lat, p2_lon = map(radians, [p1[0], p1[1], p2[0], p2[1]])

    # Haversine Formula in Python
    dlon = p2_lon - p1_lon
    dlat = p2_lat - p1_lat
    a = sin(dlat/2)**2 + cos(p1_lat) * cos(p2_lat) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    m = km * 0.621371
    return m

# check if in desired neighborhoods
def in_box(coords, box):
    if box[0][0] < coords[0] < box[1][0] and box[1][1] < coords[1] < box[0][1]:
        return True
    return False

def in_hood(location, neighborhoods):
    for n in neighborhoods:
        if n in location.lower():
            return n
    return ""

# post to slack
def post_to_slack(slack_client, listing):
    # Neighborhood variables
    area  = listing.area
    price = listing.price
    name  = listing.name
    link  = listing.link

    # Transit variables
    near_bart   = listing.near_bart
    bart_dist   = listing.bart_dist
    bart        = listing.bart_stop
    station_msg = ""

    if near_bart:
        station_msg = " | Near Bart (%s) ~ %.2fmi]" % (bart, bart_dist)
    post = "*%s* | %s%s | %s | %s" % (area, price, station_msg, name, link)

    slack_client.api_call(
        "chat.postMessage", channel=settings.SLACK_CHANNEL, text=post,
        username='hoodlum', icon_emoji=':robot_face:'
    )
