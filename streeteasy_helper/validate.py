def validate_initial_input(user_input):
    values = [item.strip() for item in user_input.split(",")]

    required = {"1","2","3"}

    if not required.issubset(set(values)):
        raise ValueError("Input must include 1,2, and 3, and are separated by commas")
    
    return values

def validate_rent_input(user_input):
    values = [item.strip() for item in user_input.split("-")]

    if len(values) != 2 or values[0] > values[1] or not values[0].isnumeric() or not values[1].isnumeric():
        raise ValueError("Input must be numeric, first value must be less than second, and are separated by dashes")
    
    return list(map(int, values))

def validate_people_input(user_input):
    if not user_input.isnumeric():
        raise ValueError("Input must be numeric")
    
    return int(user_input)