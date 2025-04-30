import requests
import os
from dotenv import load_dotenv

load_dotenv()

def create_possible_areas(zipcodes, zip_to_neighborhood_mapping):
    possible_areas = []
    for zipcode, _ in zipcodes:
        possible_areas.extend(zip_to_neighborhood_mapping.get(zipcode, []))
    
    return list(set(possible_areas))

def create_params(user_selected_neighborhoods_bool: bool, selected_neighborhoods: list, possible_zipcodes: list, validated_rent: list, validated_num_people: int, validated_num_bathroom: int, zip_to_neighborhood_mapping: dict):
    if not user_selected_neighborhoods_bool:
        possible_areas = create_possible_areas(possible_zipcodes, zip_to_neighborhood_mapping)
    else:
        possible_areas = list(set(selected_neighborhoods))

    # get min rent and max rent prices
    min_price = min(validated_rent[0] * validated_num_people, validated_rent[1] * validated_num_people)
    max_price = max(validated_rent[0] * validated_num_people, validated_rent[1] * validated_num_people)

    params = {"areas": ','.join(possible_areas), "minPrice": min_price, "maxPrice": max_price, "minBeds": validated_num_people, "minBaths": validated_num_bathroom, "limit": 10}
    return params

def create_headers():
    headers = {'x-rapidapi-host': os.getenv('API_HOST'),
                'x-rapidapi-key': os.getenv('API_KEY')}

    return headers

def query_rental_search(validated_rent: list, validated_num_people: int, validated_num_bathroom: int, zip_to_neighborhood_mapping: dict, user_selected_neighborhoods_bool: bool, possible_zipcodes: list = [], selected_neighborhoods: list = []):
    # if user didn't select neighborhood
    if not user_selected_neighborhoods_bool:
        url = "https://streeteasy-api.p.rapidapi.com/rentals/search"
        params = create_params(user_selected_neighborhoods_bool, selected_neighborhoods, possible_zipcodes, validated_rent, validated_num_people, validated_num_bathroom, zip_to_neighborhood_mapping)
        headers = create_headers()

        # resp = requests.get(url, headers=headers, params=params)
        # data = resp.json()

        # TEST DATA, USE THIS SO WE DON'T HIT OUR RATE LIMIT FOR STREETEASYAPI
        data = {'pagination': {'count': 120, 'nextOffset': 11}, 'listings': [{'id': '4717333', 'price': 4000, 'status': 'open', 'longitude': -73.97428416, 'latitude': 40.67670956, 'url': 'https://www.streeteasy.com/rental/4717333'}, {'id': '4717112', 'price': 3750, 'status': 'open', 'longitude': -73.93215663, 'latitude': 40.75905995, 'url': 'https://www.streeteasy.com/rental/4717112'}, {'id': '4716899', 'price': 3950, 'status': 'open', 'longitude': -73.9051442, 'latitude': 40.70681915, 'url': 'https://www.streeteasy.com/rental/4716899'}, {'id': '4716532', 'price': 4500, 'status': 'open', 'longitude': -73.90220887, 'latitude': 40.77523515, 'url': 'https://www.streeteasy.com/rental/4716532'}, {'id': '4716527', 'price': 4000, 'status': 'open', 'longitude': -73.91851623, 'latitude': 40.76457628, 'url': 'https://www.streeteasy.com/rental/4716527'}, {'id': '4715782', 'price': 4500, 'status': 'open', 'longitude': -73.91550354, 'latitude': 40.7547589, 'url': 'https://www.streeteasy.com/rental/4715782'}, {'id': '4715776', 'price': 4600, 'status': 'open', 'longitude': -73.97684241, 'latitude': 40.68085197, 'url': 'https://www.streeteasy.com/rental/4715776'}, {'id': '4715774', 'price': 4200, 'status': 'open', 'longitude': -73.98158174, 'latitude': 40.66123591, 'url': 'https://www.streeteasy.com/rental/4715774'}, {'id': '4715594', 'price': 4399, 'status': 'open', 'longitude': -73.90907824, 'latitude': 40.70226602, 'url': 'https://www.streeteasy.com/rental/4715594'}, {'id': '4715589', 'price': 4450, 'status': 'open', 'longitude': -73.95189483, 'latitude': 40.78317144, 'url': 'https://www.streeteasy.com/rental/4715589'}]}

        return data['listings']
    
    else: # user selected the neighborhoods beforehand
        url = "https://streeteasy-api.p.rapidapi.com/rentals/search"
        params = create_params(user_selected_neighborhoods_bool, selected_neighborhoods, possible_zipcodes, validated_rent, validated_num_people, validated_num_bathroom, zip_to_neighborhood_mapping)
        headers = create_headers()

        resp = requests.get(url, headers=headers, params=params)
        data = resp.json()

        # TEST DATA, USE THIS SO WE DON'T HIT OUR RATE LIMIT FOR STREETEASYAPI
        # data = {'pagination': {'count': 8}, 'listings': [{'id': '4719334', 'price': 6800, 'status': 'open', 'longitude': -73.95478978, 'latitude': 40.73684408, 'url': 'https://www.streeteasy.com/rental/4719334'}, {'id': '4717094', 'price': 7250, 'status': 'open', 'longitude': -73.94287476, 'latitude': 40.71149644, 'url': 'https://www.streeteasy.com/rental/4717094'}, {'id': '4717027', 'price': 6399, 'status': 'open', 'longitude': -73.95504, 'latitude': 40.70794, 'url': 'https://www.streeteasy.com/rental/4717027'}, {'id': '4713129', 'price': 8000, 'status': 'open', 'longitude': -73.94488125, 'latitude': 40.7147033, 'url': 'https://www.streeteasy.com/rental/4713129'}, {'id': '4712678', 'price': 6500, 'status': 'open', 'longitude': -73.94819641, 'latitude': 40.70920181, 'url': 'https://www.streeteasy.com/rental/4712678'}, {'id': '4711759', 'price': 6000, 'status': 'open', 'longitude': -73.95627202, 'latitude': 40.70762164, 'url': 'https://www.streeteasy.com/rental/4711759'}, {'id': '4711565', 'price': 8000, 'status': 'open', 'longitude': -73.9511558, 'latitude': 40.72736222, 'url': 'https://www.streeteasy.com/rental/4711565'}, {'id': '4678305', 'price': 7900, 'status': 'open', 'longitude': -73.95785538, 'latitude': 40.71651209, 'url': 'https://www.streeteasy.com/rental/4678305'}]}
        # data = {'pagination': {'count': 5}, 'listings': [{'id': '4717675', 'price': 8000, 'status': 'open', 'longitude': -73.95240326, 'latitude': 40.78416525, 'url': 'https://www.streeteasy.com/rental/4717675'}, {'id': '4715486', 'price': 6995, 'status': 'open', 'longitude': -73.95246613, 'latitude': 40.78209575, 'url': 'https://www.streeteasy.com/rental/4715486'}, {'id': '4715202', 'price': 6100, 'status': 'open', 'longitude': -73.95549774, 'latitude': 40.77629852, 'url': 'https://www.streeteasy.com/rental/4715202'}, {'id': '4705882', 'price': 6300, 'status': 'open', 'longitude': -73.94713653, 'latitude': 40.78198638, 'url': 'https://www.streeteasy.com/rental/4705882'}, {'id': '4697790', 'price': 8000, 'status': 'open', 'longitude': -73.95320129, 'latitude': 40.78239822, 'url': 'https://www.streeteasy.com/rental/4697790'}]}
        return data['listings']

