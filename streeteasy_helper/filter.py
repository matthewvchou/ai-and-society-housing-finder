import csv

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