
# The options of our research
# Simply remove the field in the dictionary to ignore it
SEARCH_OPTIONS = {
    'minPrice' : 5000, # minimum price in SEK
    'maxPrice' : 12000, # maximum price in SEK
    'minRooms' : 1, # minimum number of rooms
    'maxRooms' : 10, # maximum number of rooms
    'minBedrooms' : 1, # minimum number of bedrooms, the maximum can't be set as it's not appearing in the blocket results
    'minSize' : 80, # minimum size in square meters
    'maxSize' : 100 # maximum size in square meters
}

# The prefered neighboorhoods
# If not empty, will only filter offers from theses neighboorhoods
PREFERED_NEIGHBOORHOODS = [ ]

# How often should we check, in seconds
SLEEP_INTERVAL = 3
