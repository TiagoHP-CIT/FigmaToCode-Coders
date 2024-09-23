
from promptflow import tool

@tool
def process(json_obj):

    def round_border_weight(json_data):
        if isinstance(json_data, dict):
            if json_data.get('type') == 'ICON':
                if 'borderWeight' in json_data:
                    json_data['borderWeight'] = round(json_data['borderWeight'])
            
            for value in json_data.values():
                round_border_weight(value)
        
        elif isinstance(json_data, list):
            for item in json_data:
                round_border_weight(item)

        return json_data
    
    return round_border_weight(json_obj)
