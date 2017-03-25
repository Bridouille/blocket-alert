#!/usr/bin/env python3

import settings
import listing
from db import Db
from blocket import BlocketHousingRent

# Thoses constants will be used if a field is not present in the SEARCH_OPTIONS
DEFAULT_MAX_PRICE = 100000 # 100 000 SEK / monthly_rent
DEFAULT_MIN_PRICE = 1000 # 1 000 SEK / monthly_rent
DEFAULT_MAX_ROOMS = 13
DEFAULT_MIN_ROOMS = 1
DEFAULT_MAX_SIZE = 400
DEFAULT_MIN_SIZE = 10

# Returns True if the given result matches the given search options
def matchesFilters(result, options, neighboorhoods):
    if result.price > options.get('maxPrice', DEFAULT_MAX_PRICE) or result.price < options.get('minPrice', DEFAULT_MIN_PRICE):
        return False

    if result.rooms > options.get('maxRooms', DEFAULT_MAX_ROOMS) or result.rooms < options.get('minRooms', DEFAULT_MIN_ROOMS):
        return False

    if result.size > options.get('maxSize', DEFAULT_MAX_SIZE) or result.size < options.get('minSize', DEFAULT_MIN_SIZE):
        return False

    # If we have prefered neighboorhoods we check if the location is in one of them
    if len(neighboorhoods) > 0:
        goodLocation = False
        for neighboorhood in neighboorhoods:
            if neighboorhood in result.location:
                goodLocation = True
                break
        if not goodLocation:
            return False

    return True

def getNewResults():
    # Get the results from blocket
    client = BlocketHousingRent("stockholm")
    results = client.getResults(settings.SEARCH_OPTIONS, withImg = True, limit = 10)
    filteredResults = [ ]

    # Instantiate the SQlite db
    db = Db("listings.db")

    # We filter the results with our search criteria and remove the ones we already saw
    for res in results:
        if matchesFilters(res, settings.SEARCH_OPTIONS, settings.PREFERED_NEIGHBOORHOODS) and not db.isPresent(res.blocket_id):
            filteredResults.append(res)

    # We add the new filtered results to the db, and send a slack message
    for res in filteredResults:
        print("Adding result to db => " + str(res))
        db.add(res)

if __name__ == '__main__':
    # main loop
    while True:
        getNewResults()
        break
    # time.sleep(settings.SLEEP_INTERVAL)
