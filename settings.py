import os

# The options of our research
# Simply remove the field in the dictionary to ignore it
SEARCH_OPTIONS = {
    'minPrice' : 9000, # minimum price in SEK
    'maxPrice' : 12000, # maximum price in SEK
    'minRooms' : 1, # minimum number of rooms
    'maxRooms' : 3, # maximum number of rooms
    'minBedrooms' : 1, # minimum number of bedrooms, the maximum can't be set as it's not appearing in the blocket results
    'minSize' : 20, # minimum size in square meters
    'maxSize' : 80 # maximum size in square meters
}

# The city to search in Blocket.se
CITY = "stockholm"

# The prefered neighboorhoods
# If not empty, will only filter offers from theses neighboorhoods
# PREFERED_NEIGHBOORHOODS = [
#     'Vasastan',
#     'Norrmalm',
#     'Bromma'
# ]
PREFERED_NEIGHBOORHOODS = [ ]

# How often should we check, in seconds
SLEEP_INTERVAL = 20 * 60

# Slack Integration
SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]
SLACK_CHANNEL = '@nicolas'
