
from promptflow import tool
import requests
import json

@tool
def getFigmaComponent(file_key, node_ids, token) -> str:

    # Fazendo a requisição à API
    url = f"https://api.figma.com/v1/files/{file_key}/nodes?ids={node_ids}"
    headers = {
        "X-Figma-Token": token
    }

    response = requests.get(url, headers=headers)

    # Tratando a resposta
    if response.status_code == 200:
        obj_result = response.json()
        node = list(obj_result['nodes'].keys())[0]
        obj_document = obj_result['nodes'][node]['document']

        def limit_decimal_places(value: str, places: int) -> str:
            if '.' in value:
                integer_part, decimal_part = value.split('.')
                decimal_part = decimal_part.ljust(places, '0')
                return f"{integer_part}.{decimal_part[:places]}"
            return value + '.' + '0' * places

        def map_color(obj_color):
            colorR = limit_decimal_places(str(obj_color["r"]), 3)
            colorG = limit_decimal_places(str(obj_color["g"]), 3)
            colorB = limit_decimal_places(str(obj_color["b"]), 3)
            colorA = limit_decimal_places(str(obj_color["a"]), 3)
            return "r:{} g:{} b:{} a:{}".format(colorR, colorG, colorB, colorA)
        
        def map_user_interactions(obj_interaction):
            if obj_interaction:
                return [interaction['trigger']['type'] for interaction in obj_interaction]
            return None

        def map_children(obj_children, parent_x, parent_y):
            if obj_children:
                return [map_obj(child, parent_x, parent_y) for child in obj_children]
            return None

        def add_key_value(actual_data, key, value):
            actual_data[key] = value
            return actual_data

        def map_obj(obj, parent_x, parent_y):
            prop_by_name = {}
            split_name = []

            if obj['type'] == "INSTANCE":
                obj['type'] = "ICON"
            else:
                split_name = obj['name'].split(", ")

                for prop_name in split_name:
                    split_prop_name = prop_name.split("=")
                    if 2 == len(split_prop_name):
                        prop_by_name[split_prop_name[0]] = split_prop_name[1]

            obj_data = {
                "type": obj['type'],
                "size": "W:{}, H:{}".format(obj['absoluteBoundingBox']['width'], obj['absoluteBoundingBox']['height']),
            }

            if parent_x and parent_y:
                xvalue = (parent_x - obj['absoluteBoundingBox']['x']) * -1
                yvalue = (parent_y - obj['absoluteBoundingBox']['y']) * -1
                obj_data = add_key_value(obj_data, "position", "X:{}, Y:{}".format(xvalue, yvalue))

            if prop_by_name.get("Type"):
                obj_data = add_key_value(obj_data, "typeName", prop_by_name.get("Type"))

            if prop_by_name.get("Color"):
                obj_data = add_key_value(obj_data, "parentColor", prop_by_name.get("Color"))

            if prop_by_name.get("State"):    
                obj_data = add_key_value(obj_data, "State", prop_by_name.get("State"))

            if prop_by_name.get("Icon") and prop_by_name.get("Icon") == "On":
                obj_data = add_key_value(obj_data, "hasIcon", True)

            if 'backgroundColor' in obj and (obj['fills'] and obj['fills'][0] is not None):
                if  obj["backgroundColor"] == obj['fills'][0]['color']:
                    obj_data = add_key_value(obj_data, "backgroundColor", map_color(obj['backgroundColor']))
                else:
                    obj_data = add_key_value(obj_data, "backgroundColor", map_color(obj['backgroundColor']))
                    obj_data = add_key_value(obj_data, "fills", map_color(obj['fills'][0]['color']))
            else:
                if obj['fills'] and obj['fills'][0] is not None:
                    obj_data = add_key_value(obj_data, "fills", map_color(obj['fills'][0]['color']))
                if  'backgroundColor' in obj:
                    obj_data = add_key_value(obj_data, "backgroundColor", map_color(obj['backgroundColor']))


            if obj['strokeWeight']:
                obj_data = add_key_value(obj_data, "borderWeight", obj['strokeWeight'])

            if obj['strokes']:
                 obj_data = add_key_value(obj_data, "borderColor", map_color(obj['strokes'][0]['color']))

            if 'cornerRadius' in obj:
                obj_data = add_key_value(obj_data, "cornerRadius", obj['cornerRadius'])

            if obj['interactions']:
                obj_data = add_key_value(obj_data, "userInteractions", map_user_interactions(obj['interactions']))

            if 'children' in obj and obj['type'] != "ICON":
                obj_data = add_key_value(obj_data, "children", map_children(obj['children'], obj['absoluteBoundingBox']['x'], obj['absoluteBoundingBox']['y']))

            if 'style' in obj:
                obj_data = add_key_value(obj_data, "textValue", obj['characters'])
                obj_data = add_key_value(obj_data, "textFont", obj['style']['fontPostScriptName'])
                obj_data = add_key_value(obj_data, "textFontWeight", obj['style']['fontWeight'])
                obj_data = add_key_value(obj_data, "textFontSize", obj['style']['fontSize'])
                obj_data = add_key_value(obj_data, "textAlignHorizontal", obj['style']['textAlignHorizontal'])
                obj_data = add_key_value(obj_data, "textOpenTypeFlags", obj['style']['opentypeFlags'])
                obj_data = add_key_value(obj_data, "textValue", obj['characters'])
            return obj_data

        obj_variation = [map_obj(component, None, None) for component in obj_document['children'] if component['type'] == "COMPONENT"]

        obj_to_flow = {
            "variations": obj_variation
        }

        # Convertendo para String
        return obj_to_flow

    else:
        print(f"Erro ao acessar a API: {response.status_code} - {response.text}")
        return None

