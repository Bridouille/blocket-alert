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
    'maxSize' : 60, # maximum size in square meters
    'minSquareMeterPrice': 50, # minimum acceptable m2 price
    'maxSquareMeterPrice': 1000, # maximum acceptable m2 price
}

# The city to search in Blocket.se
CITY = "stockholm"

# The prefered neighboorhoods
# If not empty, will ONLY filter offers from theses neighboorhoods
# PREFERED_NEIGHBOORHOODS = [
#     'Vasastan',
#     'Norrmalm',
#     'Bromma'
# ]
PREFERED_NEIGHBOORHOODS = [ ]

# The excluded neighboorhoods
# If not empty, will ignore the offers from  theses neighboorhoods
EXCLUDED_NEIGHBOORHOODS = [
    'Täby',
    'Sollentuna',
    'Österåker',
    'Älvsjö',
    'Vallentuna',
    'Nacka',
    'Kista',
    'Tensta',
    'Sickla',
    'Huddinge',
    'Årsta'
]

# How often should we check, in seconds
SLEEP_INTERVAL = 5 * 60

# Slack Integration
SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]
SLACK_CHANNEL = '@nicolas' # Can also be a channel, '#housing' for example
