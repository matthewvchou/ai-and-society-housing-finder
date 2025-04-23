import requests
import os
from dotenv import load_dotenv

load_dotenv()

def create_possible_areas(zipcodes, zip_to_neighborhood_mapping):
    possible_areas = []
    for zipcode, _ in zipcodes:
        possible_areas.extend(zip_to_neighborhood_mapping.get(zipcode, []))
    
    return list(set(possible_areas))

def create_params(possible_zipcodes: list, validated_rent: list, validated_num_people: int, zip_to_neighborhood_mapping: dict):
    possible_areas = create_possible_areas(possible_zipcodes, zip_to_neighborhood_mapping)

    # get min rent and max rent prices
    min_price = min(validated_rent[0] * validated_num_people, validated_rent[1] * validated_num_people)
    max_price = max(validated_rent[0] * validated_num_people, validated_rent[1] * validated_num_people)

    params = {"areas": ','.join(possible_areas), "minPrice": min_price, "maxPrice": max_price, "minBeds": validated_num_people, "limit": 10}
    return params

def create_headers():
    headers = {'x-rapidapi-host': os.getenv('API_HOST'),
                'x-rapidapi-key': os.getenv('API_KEY')}

    return headers

def query_rental_search(possible_zipcodes: list, validated_rent: list, validated_num_people: int, zip_to_neighborhood_mapping: dict):
    url = "https://streeteasy-api.p.rapidapi.com/rentals/search"
    params = create_params(possible_zipcodes, validated_rent, validated_num_people, zip_to_neighborhood_mapping)
    headers = create_headers()

    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()

    # TEST DATA, USE THIS SO WE DON'T HIT OUR RATE LIMIT FOR STREETEASYAPI
    # data = {'pagination': {'count': 120, 'nextOffset': 11}, 'listings': [{'id': '4717333', 'price': 4000, 'status': 'open', 'longitude': -73.97428416, 'latitude': 40.67670956, 'url': 'https://www.streeteasy.com/rental/4717333'}, {'id': '4717112', 'price': 3750, 'status': 'open', 'longitude': -73.93215663, 'latitude': 40.75905995, 'url': 'https://www.streeteasy.com/rental/4717112'}, {'id': '4716899', 'price': 3950, 'status': 'open', 'longitude': -73.9051442, 'latitude': 40.70681915, 'url': 'https://www.streeteasy.com/rental/4716899'}, {'id': '4716532', 'price': 4500, 'status': 'open', 'longitude': -73.90220887, 'latitude': 40.77523515, 'url': 'https://www.streeteasy.com/rental/4716532'}, {'id': '4716527', 'price': 4000, 'status': 'open', 'longitude': -73.91851623, 'latitude': 40.76457628, 'url': 'https://www.streeteasy.com/rental/4716527'}, {'id': '4715782', 'price': 4500, 'status': 'open', 'longitude': -73.91550354, 'latitude': 40.7547589, 'url': 'https://www.streeteasy.com/rental/4715782'}, {'id': '4715776', 'price': 4600, 'status': 'open', 'longitude': -73.97684241, 'latitude': 40.68085197, 'url': 'https://www.streeteasy.com/rental/4715776'}, {'id': '4715774', 'price': 4200, 'status': 'open', 'longitude': -73.98158174, 'latitude': 40.66123591, 'url': 'https://www.streeteasy.com/rental/4715774'}, {'id': '4715594', 'price': 4399, 'status': 'open', 'longitude': -73.90907824, 'latitude': 40.70226602, 'url': 'https://www.streeteasy.com/rental/4715594'}, {'id': '4715589', 'price': 4450, 'status': 'open', 'longitude': -73.95189483, 'latitude': 40.78317144, 'url': 'https://www.streeteasy.com/rental/4715589'}]}

    return data['listings']