import requests


class Weather:
    """Creates a Weather object getting an apikey as input
    and either a city name or lat and lon coordinates.

    Package use example:

    # Create a weather object using a city name:
    # The api key below is not guaranteed to work.
    # Get your own apikey from https://openweathermap.org
    # And wait a couple of hours for the apikey to be activated

    >>> weather1 = Weather(apikey='71bafeefe82e26ce9eebc1bf9ea8293b', city='Seattle')

    # Using latitude and longitude coordinates
    >>> weather2 = Weather(apikey='71bafeefe82e26ce9eebc1bf9ea8293b', lat=41.1, lon=25)

    # Get complete weather data for the next 12 hours:
    >>> weather1.next_12h()

    # Simplified data for the next 12 hours:
    >>> weather1.next_12h_simplified()
    """

    def __init__(self, apikey, city=None, lat=None, lon=None):
        if city:
            url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=imperial'
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}&units=imperial'
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("provide either a city or lat and lon arguments")

        if self.data['cod'] != '200':
            raise ValueError(self.data['message'])

    def next_12h(self):
        """Returns 3-hour data for the next 12 hours as a dict."""
        return self.data['list'][:4]

    def next_12h_simplified(self):
        """Returns date, temperature, and sky condition every 3 hours
        for the next 12 hours as a tuple of tuples"""
        simple_data = []
        for i in self.data['list'][:4]:
            simple_data.append((i['dt_txt'], i['main']['temp'], i['weather'][0]['description']))
        return simple_data
