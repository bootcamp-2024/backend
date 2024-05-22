from apify_client import ApifyClient
import json
import os
import nltk

nltk.download('punkt')  

FRACTIONS = {
"\u00BD": 0.5,  # ½
"\u2153": 0.33,  # ⅓
"\u2154": 0.66,  # ⅔
"\u00BC": 0.25,  # ¼
"\u00BE": 0.75,  # ¾
"\u2159": 0.125,  # ⅛
"\u215B": 0.375,  # ⅜
"\u215C": 0.625,  # ⅝
"\u215E": 0.875,  # ⅞
}


URL = [
    [   "https://www.allrecipes.com/recipes/698/world-cuisine/asian/indonesian/"    ],
    [   "https://www.allrecipes.com/recipes/1879/world-cuisine/asian/indian/desserts/",
        "https://www.allrecipes.com/recipes/1877/world-cuisine/asian/indian/side-dishes/",
        "https://www.allrecipes.com/recipes/1876/world-cuisine/asian/indian/bread/",
        "https://www.allrecipes.com/recipes/1874/world-cuisine/asian/indian/appetizers/",
        "https://www.allrecipes.com/recipes/17136/world-cuisine/asian/indian/main-dishes/",
        "https://www.allrecipes.com/recipes/15935/world-cuisine/asian/indian/drinks/"   ],
    [   "https://www.allrecipes.com/recipes/17825/world-cuisine/asian/thai/main-dishes/pad-thai/",
        "https://www.allrecipes.com/recipes/23014/world-cuisine/asian/thai/desserts/",
        "https://www.allrecipes.com/recipes/1898/world-cuisine/asian/thai/soups-and-stews/",
        "https://www.allrecipes.com/recipes/1894/world-cuisine/asian/thai/appetizers/",
        "https://www.allrecipes.com/recipes/17137/world-cuisine/asian/thai/main-dishes/"    ],
    [   "https://www.allrecipes.com/recipes/701/world-cuisine/asian/malaysian/"     ],
    [   "https://www.allrecipes.com/recipes/17490/world-cuisine/asian/japanese/appetizers/",
        "https://www.allrecipes.com/recipes/17491/world-cuisine/asian/japanese/main-dishes/",
        "https://www.allrecipes.com/recipes/17492/world-cuisine/asian/japanese/soups-and-stews/"    ],
    [   "https://www.allrecipes.com/recipes/17833/world-cuisine/asian/korean/main-dishes/",
        "https://www.allrecipes.com/recipes/17832/world-cuisine/asian/korean/soups-and-stews/" ],
    [   "https://www.allrecipes.com/recipes/259/main-dish/stir-fry/",
        "https://www.allrecipes.com/recipes/1900/world-cuisine/asian/chinese/soups-and-stews/",
        "https://www.allrecipes.com/recipes/1899/world-cuisine/asian/chinese/appetizers/",
        "https://www.allrecipes.com/recipes/17135/world-cuisine/asian/chinese/main-dishes/"     ],
    [   "https://www.allrecipes.com/recipes/703/world-cuisine/asian/vietnamese/"    ]
]

CUISINE = [
    "Indonesian",
    "Indian",
    "Thai",
    "Malaysian",
    "Japanese",
    "Korean",
    "Chinese",
    "Vietnamese"
]

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
        if "(" in unit and ")" in parts[0]:
            unit += " " + parts[0]
            parts = parts[1:]

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

def Per_Cuisine_Crawler(crawl_urls, cuisine):
    '''
    Crawl recipe in each Asian cuisine
    Input:
        crawl_url: link to crawl recipe, one link is one cuisine in URL list
        cuisine: name of crawling cuisine (country name)
    Output:
        List of recipes with number of result log
    '''

    # Initialize the ApifyClient with your API token
    client = ApifyClient("apify_api_KeqCx8eA8w6cp6jNXQIezKpOBY4fJZ0LwLcs")
    recipes = []
    
    for crawl_url in crawl_urls:
        # Prepare the Actor input
        run_input = {
            "startUrls": [crawl_url],
            "maxItems": 500,
            "proxy": { "useApifyProxy": True },
        }

        # Run the Actor and wait for it to finish
        run = client.actor("iw2Kd0eeiv2DNadMk").call(run_input=run_input)

        # Fetch and print Actor results from the run's dataset (if there are any)


        category = crawl_url.split('/')[-2]     #Category in last / of url
        if category == cuisine.lower():
            category = "main-dishes"

        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            item['cuisine'] = cuisine
            item['category'] = category
            extracted_ingredients = []
            for ingredient in item['ingredients']:
                extracted_ingredients.append(extract_ingredient_info(ingredient))
            item['ingredients'] = extracted_ingredients
            recipes.append(item)

    print("Finish crawing " + cuisine + " recipes with " + str(len(recipes)) + " results!")
    return recipes

def Recipe_Crawler():
    '''
    Crawl all recipes, loop through each link and cuisine to crawl
    Output:
        File json with file name is cuisine.json
    '''
    all_recipes = []
    save_path = os.path.join(os.getcwd(), 'Data', 'Crawled', 'Recipes')
    for index in range(len(CUISINE)):
        # print(URL[index], CUISINE[index])
        recipes = Per_Cuisine_Crawler(URL[index], CUISINE[index])
        all_recipes.extend(recipes)

        file_name = 'Recipes.json'
        file_dir = os.path.join(save_path, file_name)
        with open(file_dir, 'w') as f:
            json.dump(all_recipes, f, indent=4, ensure_ascii=True)
    
    
Recipe_Crawler()