
from bs4 import BeautifulSoup
from listing import Listing
import requests

# This class is used to get a list of blocket ads for renting places
# You can query only ads with images, and set the minimum size, number of rooms and bedrooms
class BlocketHousingRent:
    def __init__(self, location = "stockholm"):
        self.url = 'https://www.blocket.se/bostad/uthyres/' + location
        self.roomsToRos = { '1' : 1, '1.5' : 2, '2' : 3, '2.5' : 4, '3' : 5, '3.5' : 6,
                            '4' : 7, '5' : 8, '6' : 9, '7' : 10, '8' : 11, '9' : 12, '10' : 13 }
        # Thoses constants will be used if the option is not well formated
        self.DEFAULT_MIN_ROOMS = 1
        self.DEFAULT_MIN_SIZE = 10
        self.DEFAULT_MIN_BEDROOMS = 1

    # Get the minimum size of the appartment
    # Return the corresponding GET parameter for blocket
    def getMinSize(self, minSize = 0):
        if minSize < 0:
            return 0
        return minSize // 10 - 1 if minSize // 10 - 1 <= 17 else 17 # 17 = 180m2

    # Get the number of rooms and return the corresponding GET parameter for blocket
    def getMinRooms(self, minRooms = 1):
        if minRooms < 0:
            return 1
        try:
            return self.roomsToRos[str(minRooms)]
        except KeyError:
            return 1

    # Get the options in the settings and return the proper GET query parameters
    def formatQueryParameters(self, options = {}, page = 0):
        payload = {
            'ss' : self.getMinSize(options.get('minSize', self.DEFAULT_MIN_SIZE)),
            'ros' : self.getMinRooms(options.get('minRooms', self.DEFAULT_MIN_ROOMS)),
            'bs' : options.get('minBedrooms', self.DEFAULT_MIN_BEDROOMS),
            'o' : page
        }
        return payload

    # Get the results from blocket corresponding to the given options
    # You can filter to get only ads with images
    # The limit parameter is the number of results
    # The option dict should be like this, with the blocket parameters :
    # options = {
    #     minSize : 20,
    #     minRooms : 1.5,
    #     minBedrooms : 2
    # }
    def getResults(self, options = {}, withImg = False, limit = 30):
        results = [ ]
        page = 0

        while len(results) < limit:
            payload = self.formatQueryParameters(options, page)
            page += 1
            r = requests.get(self.url, params = payload)
            soup = BeautifulSoup(r.content, 'html.parser')

            for item in soup.find_all('div', { 'class' : 'item_row' }):
                if len(results) >= limit:
                    break

                id = item.attrs['id']
                hasImg = False if item.find_all('div', { 'class' : 'no-image' }) else True
                if withImg == True and hasImg == False: # We don't want to keep the ad since it hasn't images
                    continue

                # Retrieve the type of housing, and the approx location
                category = item.find('span', { 'class' : 'category' }).text.strip()
                location = item.find('span', { 'class' : 'address'}).text.strip()

                # Retrieve the name and the link to the add
                header = item.find('a', { 'class' : 'item_link' })
                name = header.text.strip()
                link = header.get('href')

                # Retrieve number of rooms, price and size
                details = item.find('div', { 'class' : 'details' })
                priceSpan = details.find('span', { 'class' : 'monthly_rent'})
                price = int(priceSpan.text.strip()[:-7].replace(' ', '')) if priceSpan is not None else -1
                sizeSpan = details.find('span', { 'class' : 'size'})
                size = int(float(sizeSpan.text.strip()[:-3].replace(',', '.')) // 1) if sizeSpan is not None else -1
                roomsSpan = details.find('span', { 'class' : 'rooms'})
                rooms = float(roomsSpan.text.strip()[:-4].replace(',', '.')) if roomsSpan is not None else -1

                # Retrive the date when the ad was posted
                dateTime = item.find('time', { 'class' : 'jlist_date_image' })
                date = dateTime.attrs['datetime'] if dateTime is not None else -1

                result = Listing(
                    blocket_id = id,
                    category = category,
                    location = location,
                    name = name,
                    link = link,
                    price = price,
                    size = size,
                    rooms = rooms,
                    date = date
                )
                results.append(result)

        return results
