
from promptflow import tool
import json
import re

@tool
def replace_values(json_obj, json_font):
   
    def get_fonts(json_data):
        content_str = json_data['choices'][0]['message']['content']
        return json.loads(content_str)
    
    def process(json_data, font_mappings):
        if isinstance(json_data, dict):
            if json_data.get('type') == 'TEXT':
                text_font = json_data.get('textFont')
                text_font_size = json_data.get('textFontSize')
                font_result = None
                
                for mapping in font_mappings:
                    match = re.match(r'(.+) = (.+):(\d+)', mapping)
                    if match:
                        property_value, font_name, size = match.groups()
                        if font_name == text_font and int(size) == text_font_size:
                            font_result = property_value
                            break
                
                if font_result:
                    json_data['font'] = font_result
                    keys_to_remove = ['textValue', 'textFont', 'textFontWeight', 'textFontSize', 'textAlignHorizontal', 'textOpenTypeFlags']
                    for key in keys_to_remove:
                        json_data.pop(key, None)
            
            for value in json_data.values():
                process(value, font_mappings)
        
        elif isinstance(json_data, list):
            for item in json_data:
                process(item, font_mappings)
        
        return json_data
    
    return process(json_obj, get_fonts(json_font))


