
from promptflow import tool
import json
import re

@tool
def replace_values(json_obj, string_array):
    # Create a dictionary to map values in the format "r:value g:value b:value a:value"
    # to their respective properties
    mapping = {}
    
    # Fill the dictionary with the mappings from the string array
    for item in string_array:
        # Split the string into property and value
        if '=' in item:
            property_name, value = item.split('=', 1)
            mapping[value.strip()] = property_name.strip()
    
    # Recursive function to traverse the JSON
    def traverse_json(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    traverse_json(value)
                else:
                    # Check if the value is in the format "r:value g:value b:value a:value"
                    if isinstance(value, str) and re.match(r'^r:\d+\.\d+\s+g:\d+\.\d+\s+b:\d+\.\d+\s+a:\d+\.\d+$', value):
                        
                        valueToChange = ""

                        if value == "r:0.000 g:0.000 b:0.000 a:0.000":
                            valueToChange = "r:0.035 g:0.043 b:0.043 a:1.000"
                        else:
                            valueToChange = value

                        # If the valueToChange is in the mapping, replace it
                        if valueToChange in mapping:
                            obj[key] = mapping[valueToChange]
        elif isinstance(obj, list):
            for item in obj:
                traverse_json(item)

    # Start the search and replacement in the JSON
    traverse_json(json_obj)
    return json_obj
