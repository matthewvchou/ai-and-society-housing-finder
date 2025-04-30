import csv
import difflib
from streeteasy_helper.validate import validate_boolean_input
from streeteasy_helper.zipcode import read_in_neighborhoods

def filter_possible_neighborhoods(user_input, input_mappings):
    # sample_validate_input = ['safety_rank', 'livability_rank', 'price']
    possible_zipcodes = []
    ranges = [(0,59), (0, 119), (0,178)]

    # get index
    safety_index = user_input.index("safety_rank")
    livability_index = user_input.index("livability_rank")

    # get range
    safety_range = ranges[safety_index]
    livability_range = ranges[livability_index]

    # read csv and find possible zipcodes
    with open("models/rankings.csv", 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for zipcode, _, _, safety_rank, livability_rank in reader:
            # 3 = safety, 4 = livability
            if safety_range[0] <= int(safety_rank) <= safety_range[1] and livability_range[0] <= int(livability_rank) <= livability_range[1]:
                possible_zipcodes.append((int(zipcode), int(safety_rank) + int(livability_rank)))

    return possible_zipcodes

def select_neighborhoods(user_selected_neighborhoods_bool, selected_neighborhoods):
    if user_selected_neighborhoods_bool:
        print("Cool! Glad you have an idea of where you want to live. Please type in the neighborhood like this (upper-east-side,gramercy-park,soho)")
        print("You can view all possible options here:\n")
        print("https://jsonblob.com/1365134823747936256")
        print("Please enter each option individually. Type D to be done.")

        all_neighborhoods = read_in_neighborhoods() 
        while True:
            neighborhood_input = input()
            
            # user done
            if neighborhood_input == 'D':
                print("Gathering results based off your neighborhoods...")
                break

            # typed in exactly correct
            if neighborhood_input in all_neighborhoods:
                if neighborhood_input in selected_neighborhoods:
                    print(f'Already added {neighborhood_input}.')
                    continue
                selected_neighborhoods.append(neighborhood_input)
                print(f'Added {neighborhood_input} to selected neighborhoods! Keep going!')
            # see if there is a close match, prompt user if they want to include this.
            else:
                try:
                    close_match = difflib.get_close_matches(neighborhood_input, all_neighborhoods, 1, cutoff=0.7)[0]
                    if close_match:
                        print(f'Sorry, couldn\'t find that. Did you mean {close_match}? (Y/N)')
                        while True:
                            try:
                                is_close_match = input()
                                is_close_match = validate_boolean_input(is_close_match)
                                if is_close_match == 'y':
                                    if close_match in selected_neighborhoods:
                                        print(f'Already added {close_match}.')
                                        break
                                    selected_neighborhoods.append(close_match)
                                    print(f'Added {close_match} to selected neighborhoods!')
                                else:
                                    print("Sorry, try again.")
                                break
                            except ValueError as e:
                                print("Please type in Y/N to confirm your answer.")
                except IndexError as e:
                    print("Sorry, couldn't find a close match. Try again.")