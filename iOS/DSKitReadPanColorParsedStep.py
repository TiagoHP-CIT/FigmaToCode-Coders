from promptflow import tool
import re

@tool
def convert_color(swift_code_list) -> str:

    def limit_decimal_places(value: str, places: int) -> str:
        if '.' in value:
            integer_part, decimal_part = value.split('.')
            decimal_part = decimal_part.ljust(places, '0')
            return f"{integer_part}.{decimal_part[:places]}"
        return value + '.' + '0' * places

    colors = []
    class_name = "PanColor"  # Class name

    # Join the lines into a single string
    content = "\n".join(swift_code_list)

    # Regex to find colors defined in the style #colorLiteral
    pattern = r'public static let (\w+) = #colorLiteral\(red:\s*([0-9]*\.?[0-9]+),\s*green:\s*([0-9]*\.?[0-9]+),\s*blue:\s*([0-9]*\.?[0-9]+),\s*alpha:\s*([0-9]*\.?[0-9]+)\)'

    # Find all colors
    for match in re.finditer(pattern, content):
        property_name = match.group(1)
        r = match.group(2)
        g = match.group(3)
        b = match.group(4)
        a = match.group(5)

        # Limit the decimal places
        decimalMax = 1
        r = limit_decimal_places(r, decimalMax)
        g = limit_decimal_places(g, decimalMax)
        b = limit_decimal_places(b, decimalMax)
        a = limit_decimal_places(a, decimalMax)

        # Format the string
        formatted_color = f"{class_name}.{property_name}=r:{r} g:{g} b:{b} a:{a}"
        colors.append(formatted_color)

    return colors