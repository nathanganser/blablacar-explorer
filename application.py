import requests
import os
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from geopy import distance
import datetime
import math

from dateutil import parser
load_dotenv()


geolocator = Nominatim(user_agent="blabla")



def make_call(from_coordinate, to_coordinate, start_date):
    url = f"https://public-api.blablacar.com/api/v3/trips?from_coordinate={from_coordinate.latitude},{from_coordinate.longitude}&to_coordinate={to_coordinate.latitude},{to_coordinate.longitude}&locale=fr-FR&currency=EUR&start_date_local={start_date}&key={os.environ['key']}"

    payload = {}
    headers = {

    }

    response = requests.request("GET", url, headers=headers, data = payload)

    return response.json()



#search_week("Lausanne, Switzerland", "Milan, Italy")

trip_array = [{'link': 'https://www.blablacar.fr/trip?source=CARPOOLING&id=2230590546-milano-vevey', 'waypoints': [{'date_time': '2021-07-12T17:00:00', 'place': {'city': 'Milan', 'address': "Gare de Milan-Centrale, Piazza Duca d'Aosta, 1, Milano MI", 'latitude': 45.48701, 'longitude': 9.205479, 'country_code': 'IT'}}, {'date_time': '2021-07-12T21:10:00', 'place': {'city': 'Vevey', 'address': 'Vevey, gare, Vevey', 'latitude': 46.46249, 'longitude': 6.842269, 'country_code': 'CH'}}], 'price': {'amount': '19.00', 'currency': 'EUR'}, 'vehicle': {'make': 'AUDI', 'model': 'Q2'}, 'distance_in_meters': 295518, 'duration_in_seconds': 15000}, {'link': 'https://www.blablacar.fr/trip?source=CARPOOLING&id=2229754501-milano-losanna', 'waypoints': [{'date_time': '2021-07-12T19:10:00', 'place': {'city': 'Milan', 'address': 'Assago Milanofiori Nord, Milano MI', 'latitude': 45.409454, 'longitude': 9.150046, 'country_code': 'IT'}}, {'date_time': '2021-07-13T00:10:00', 'place': {'city': 'Lausanne', 'address': 'Rue du Lac 14, Lausanne', 'latitude': 46.5075, 'longitude': 6.625804, 'country_code': 'CH'}}], 'price': {'amount': '23.00', 'currency': 'EUR'}, 'vehicle': {'make': 'AUDI', 'model': 'Q5'}, 'distance_in_meters': 325555, 'duration_in_seconds': 18000}, {'link': 'https://www.blablacar.fr/trip?source=CARPOOLING&id=2231152556-milano-lausanne', 'waypoints': [{'date_time': '2021-07-15T18:00:00', 'place': {'city': 'Milan', 'address': 'Piazzale Segesta, 4, Milano MI', 'latitude': 45.475887, 'longitude': 9.138547, 'country_code': 'IT'}}, {'date_time': '2021-07-15T23:20:00', 'place': {'city': 'Lausanne', 'address': 'Gare Lausanne, Place de la Gare, Lausanne', 'latitude': 46.51683, 'longitude': 6.628691, 'country_code': 'CH'}}], 'price': {'amount': '16.00', 'currency': 'EUR'}, 'distance_in_meters': 332067, 'duration_in_seconds': 19200}]

def display_data(trip_array, location_from, location_to, ):
    for trip in trip_array:
        start_time = parser.parse(trip['waypoints'][0]['date_time'])
        end_time = parser.parse(trip['waypoints'][-1]['date_time'])
        start_distance = distance.distance((trip['waypoints'][0]['place']['latitude'], trip['waypoints'][0]['place']['longitude']), (location_from.latitude, location_from.longitude)).km
        end_distance = distance.distance((trip['waypoints'][-1]['place']['latitude'], trip['waypoints'][-1]['place']['longitude']), (location_to.latitude, location_to.longitude)).km

        print(f"{trip['waypoints'][0]['place']['city']} ({math.ceil(start_distance)} km away) - {trip['waypoints'][-1]['place']['city']} ({math.ceil(end_distance)} km away), from {start_time} to {end_time}. link: {trip['link']}")


def search_week(from_string, to_string):
    print(f'Here are all the trips found from {from_string} to {to_string}')
    location_to = geolocator.geocode(to_string)
    location_from = geolocator.geocode(from_string)
    start_date = datetime.datetime.now()
    trip_array = []
    for i in range(0, 7, +1):
        trips = make_call(location_from, location_to, start_date.isoformat()).get('trips')
        trip_array += trips
        start_date = start_date + datetime.timedelta(days=1)
    display_data(trip_array, location_from, location_to)

search_week("Paris, France", "Geneve, Suisse")