from dateutil.parser import parse


def validate(input_data, valid_keys, required_keys=[], validations={}):
    errors = ["'{}' is an invalid key.".format(key) for key in input_data if key not in valid_keys]
    errors.extend(["The '{}' field cannot be empty.".format(key) for key in required_keys if
                   (key not in input_data) or (not input_data[key])])

    custom_validation_errors = ["{}: {}".format(key, error) for key in input_data if key in validations for error in
                                validations[key](input_data[key])]
    errors.extend(custom_validation_errors)

    return errors


def validate_date(input_data):
    try:
        parse(input_data)
        return []
    except ValueError:
        return ["Failed to parse as date."]


def validate_grade(input_data):
    return [] if input_data in ['A', 'B', 'C'] else ["The grade must be A, B, or C."]


def validate_int(input_data):
    try:
        i = int(input_data)
        return [] if i >= 0 else ["Must be nonnegative."]
    except ValueError:
        return ["Failed to parse as integer."]
