#!/usr/bin/env python3

import settings
import listing
import time
import sys
from db import Db
from blocket import BlocketHousingRent
from slackclient import SlackClient

# Thoses constants will be used if a field is not present in the SEARCH_OPTIONS
DEFAULT_MAX_PRICE = 100000 # 100 000 SEK / monthly_rent
DEFAULT_MIN_PRICE = 1000 # 1 000 SEK / monthly_rent
DEFAULT_MAX_ROOMS = 13
DEFAULT_MIN_ROOMS = 1
DEFAULT_MAX_SIZE = 400
DEFAULT_MIN_SIZE = 10

# Returns True if the given result matches the given search options
def matchesFilters(result):
    options = settings.SEARCH_OPTIONS

    if not options.get('minPrice', DEFAULT_MIN_PRICE) < result.price < options.get('maxPrice', DEFAULT_MAX_PRICE):
        return False

    if not options.get('minRooms', DEFAULT_MIN_ROOMS) < result.rooms < options.get('maxRooms', DEFAULT_MAX_ROOMS):
        return False

    if not options.get('minSize', DEFAULT_MIN_SIZE) < result.size < options.get('maxSize', DEFAULT_MAX_SIZE):
        return False


    minSquareMeterPrice = options.get('minSquareMeterPrice')
    maxSquareMeterPrice = options.get('maxSquareMeterPrice')
    # Optional arguments, we only do this if the user cares about both the minimum and maximum m2 price
    if minSquareMeterPrice and maxSquareMeterPrice:
        if not minSquareMeterPrice < round(result.price/result.size) < maxSquareMeterPrice:
            return False

    # If we have prefered neighboorhoods we check if the location is in one of them
    if len(settings.PREFERED_NEIGHBOORHOODS) > 0:
        goodLocation = False
        for neighboorhood in settings.PREFERED_NEIGHBOORHOODS:
            if neighboorhood in result.location.split():
                goodLocation = True
                break
        if not goodLocation:
            return False

    # If the location is on a neighboorhood we don't want to live in, ignore it
    if len(settings.EXCLUDED_NEIGHBOORHOODS) > 0:
        for neighboorhood in settings.EXCLUDED_NEIGHBOORHOODS:
            if neighboorhood in result.location.split():
                return False

    return True

def postMessageOnSlack(sc, result, adress):
    desc = ":house: [{}] in *{}* -- posted at {}\n".format(result.name, result.location, result.date)
    desc += ":moneybag: *{}* SEK/month for *{}* m2 and *{}* rooms\n".format(result.price, result.size, result.rooms)
    desc += "See more :point_right: <{}|blocket link>".format(result.link)
    if len(adress) > 0:
        desc += " location :earth_americas: <{}|map>".format("http://maps.google.com/?q={}".format(adress))
    desc += '\n'
    resp = sc.api_call(
        "chat.postMessage",
        channel = settings.SLACK_CHANNEL,
        text = desc,
        username = 'Blocket-Alert',
        icon_emoji = ':robot_face:'
    )

def getNewResults(bc, sc, db):
    results = bc.getResults(settings.SEARCH_OPTIONS, withImg = True)
    filteredResults = [ ]

    # We filter the results with our search criteria and remove the ones we already saw
    for res in results:
        if matchesFilters(res) and not db.isPresent(res.blocket_id):
            filteredResults.append(res)

    # We add the new filtered results to the db, and send a slack message
    for res in filteredResults:
        postMessageOnSlack(sc, res, bc.getAdress(res.link)) # We only get the adress after we filtered everything
        db.add(res)

# Main loop either sleep here or add this to a crontab
if __name__ == '__main__':
    # Create a slack client
    sc = SlackClient(settings.SLACK_API_TOKEN)

    # Instantiate the SQlite db
    db = Db("listings.db", echo = True)

    # Create a Blocket client
    bc = BlocketHousingRent(settings.CITY)
    while True:
        print("{} >> Time to get new results for {}".format(time.ctime(), settings.CITY.upper()))
        getNewResults(bc, sc, db)
        print("{} >> Sleeping for {} sconds..".format(time.ctime(), settings.SLEEP_INTERVAL))
        time.sleep(settings.SLEEP_INTERVAL)
