from dateutil.parser import parse

def validate(input, valid_keys, required_keys=[], validations = {}):
    errors = ["'{}' is an invalid key.".format(key) for key in input if key not in valid_keys]
    errors.extend(["The '{}' field cannot be empty.".format(key) for key in input if key in required_keys and not input[key]])
    
    for key in input:
        if key in validations:
            error = validations[key](input[key])
            if error: 
                errors.append("{}: {}".format(key, error))
            
    return errors
    
def validate_date(input):
    try:
        parse(input)
        return None
    except ValueError:
        return "Failed to parse as date."
    