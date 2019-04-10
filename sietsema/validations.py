from dateutil.parser import parse

def validate(input, valid_keys, required_keys=[], validations = {}):
    errors = ["'{}' is an invalid key.".format(key) for key in input if key not in valid_keys]
    errors.extend(["The '{}' field cannot be empty.".format(key) for key in required_keys if (key not in input) or (not input[key])])
    
    custom_validation_errors = ["{}: {}".format(key, error) for key in input if key in validations for error in validations[key](input[key])]
    errors.extend(custom_validation_errors)
            
    return errors
    
def validate_date(input):
    try:
        parse(input)
        return []
    except ValueError:
        return ["Failed to parse as date."]

def validate_grade(input):
    return [] if input in ['A', 'B', 'C'] else ["The grade must be A, B, or C."]
    
def validate_int(input):
    try:
        int(input)
        return []
    except ValueError:
        return ["Failed to parse as integer."]