import csv
import requests
from streeteasy_helper.validate import validate_initial_input, validate_rent_input, validate_people_input
from streeteasy_helper.filter import filter_possible_neighborhoods
from streeteasy_helper.zipcode import create_zip_to_neighborhood, get_all_neighborhoods_from_listings
from streeteasy_helper.query_streeteasy import query_rental_search
from reddit_helper.reddit import search_asknyc
            
def main():
    print('Hello! Welcome to our housing finder. Please rank the 3 of these in order of importance. \nPleae make sure they are comma separated (1,2,3). First number = highest priority')
    print("1. Safety\n2. Livability\n3. Price")
    while True:
        try:
            input_str = input()
            global validated_initial 
            validated_initial = validate_initial_input(input_str)
            break
        except ValueError as e:
            print(f"Error: {e}")
            print("Please retry:")
            
    input_mappings = {"1": "safety_rank", "2": "livability_rank", "3": "price"}

    # filter
    validated_initial = [input_mappings[item] for item in validated_initial]
    possible_zipcodes = sorted(filter_possible_neighborhoods(validated_initial, input_mappings), key=lambda x: x[1])

    # validate rent
    print("Thanks! Now filter how much you want to spend on rent (per person). Please enter it like this (1500-2500)")
    while True:
        try:
            per_person_rent_input = input()
            global validated_rent
            validated_rent = validate_rent_input(per_person_rent_input)
            break
        except ValueError as e:
            print(f"Error: {e}")
            print("Please retry:")
    
    # validate number of people
    print("How many people including yourself will be in this place?")
    while True:
        try:
            num_people_input = input()
            global validated_num_people
            validated_num_people = validate_people_input(num_people_input)
            break
        except ValueError as e:
            print(f"Error: {e}")
            print("Please retry:")

    # map every zip code to a specific group of neighborhoods for passing into StreetEasyAPI
    zip_to_neighborhood_mapping = create_zip_to_neighborhood()

    # get rental searches
    listings = query_rental_search(possible_zipcodes, validated_rent, validated_num_people, zip_to_neighborhood_mapping)

    # reverse listing latitudes and longitudes to zipcodes
    neighborhood_url_mapping = get_all_neighborhoods_from_listings(listings, zip_to_neighborhood_mapping)

    # REDDIT / LLM sentiment analysis
    search_asknyc(neighborhood_url_mapping)


if __name__ == '__main__':
    main()
