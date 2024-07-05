def compare_dictionaries(dict1, dict2):
    def convert_to_common_type(value):
        # Attempt to convert the value to float, otherwise keep it as is
        try:
            return float(value)
        except ValueError:
            return value

    # Keys only in dict1
    only_in_dict1 = dict1.keys() - dict2.keys()
    # Keys only in dict2
    only_in_dict2 = dict2.keys() - dict1.keys()
    
    # Keys with different values, converting to common types for comparison
    different_values = {
        k: (dict1[k], dict2[k])
        for k in dict1.keys() & dict2.keys()
        if convert_to_common_type(dict1[k]) != convert_to_common_type(dict2[k])
    }
    
    discrepancies = {
        "only_in_dict1": {k: dict1[k] for k in only_in_dict1},
        "only_in_dict2": {k: dict2[k] for k in only_in_dict2},
        "Number of different values: ": len(different_values),
        "different_values": different_values
    }
    
    return discrepancies