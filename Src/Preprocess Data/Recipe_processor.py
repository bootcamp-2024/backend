import nltk
import json
import os
from Utils import FRACTIONS, UNIT, Read_Directory

nltk.download('punkt')  


def extract_ingredient_info(ingredient_string):
    """
    Extracts quantity, unit, and name from an ingredient string.

    Args:
        ingredient_string: The string representing an ingredient.

    Returns:
        A dictionary containing:
            quantity: The extracted quantity (e.g., "1", "¼").
            unit: The extracted unit (e.g., "cup", "ounce").
            name: The extracted ingredient name (e.g., "warm water", "active dry yeast").
    """
    #Replace all fraction
    for key, value in FRACTIONS.items():
        ingredient_string = ingredient_string.replace(key, str(value))

    parts = ingredient_string.split(" ")  # Split on spaces

    # Extract quantity (first split or second if number/fraction)
    quantity = 0
    flag = False
    while len(parts) > 1 and is_number(parts[0]):
        quantity += float(parts[0])
        parts = parts[1:]  # Remove used parts from remaining list
        flag =  True

    # Extract unit (next split, empty if " ")
    unit = ""
    if flag:
        if len(parts) > 0 and (" ") not in parts[0]:
            unit = parts[0]
            parts = parts[1:]  # Remove used parts from remaining list
        if "(" in unit and find_text(parts, ")"):
            unit += " " + " ".join(parts[0:find_text(parts, ")")])
            parts = parts[find_text(parts, ")"):]

    parts = " ".join(parts).split(",")
    name = parts[0]
    prepare_type = ",".join(parts[1:])

    return {
        "quantity": quantity,
        "unit": unit,
        "name": name.strip(),  # Remove leading/trailing whitespaces
        "prepare_type": prepare_type.strip()
    }

def is_number(text):
    """
    Checks if a string is a number or a fraction.

    Args:
        text: The string to check.

    Returns:
        True if the string is a number or a fraction, False otherwise.
    """
    try:
        float(text)
        return True
    except ValueError:
        return False
    
def find_text(list, text):
    for i in range(len(list)):
        if list[i].find(text):
            return i

database = Read_Directory(save_path)

for item in database:
    extracted_ingredients = []
    for ingredient in item['ingredients']:
        extracted_ingredients.append(extract_ingredient_info(ingredient))
    item['ingredients'] = extracted_ingredients
    

