def validate_initial_input(user_input):
    values = [item.strip() for item in user_input.split(",")]

    required = {"1","2","3"}

    if not required.issubset(set(values)):
        raise ValueError("Input must include 1,2, and 3, and are separated by commas")
    
    return values

def validate_rent_input(user_input):
    values = [item.strip() for item in user_input.split("-")]

    if len(values) != 2 or not values[0].isnumeric() or not values[1].isnumeric() or int(values[0]) > int(values[1]):
        raise ValueError("Input must be numeric, first value must be less than second, and are separated by dashes")
    
    return list(map(int, values))

def validate_integer_input(user_input):
    if not user_input.isnumeric():
        raise ValueError("Input must be numeric")
    
    return int(user_input)

def validate_boolean_input(user_input):
    possible = ['y', 'n']
    if user_input.lower() not in possible:
        raise ValueError("Input must be Y/N.")
    
    return user_input.lower()