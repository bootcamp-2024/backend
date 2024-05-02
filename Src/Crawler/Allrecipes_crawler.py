from apify_client import ApifyClient
import json
import os

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
    client = ApifyClient("apify_api_dVVQ5w9MhasXrCO5SPGTurSJr2fyBg1uIq7b")
    recipes = []
    
    for crawl_url in crawl_urls:
        # Prepare the Actor input
        run_input = {
            "startUrls": [crawl_url],
            "maxItems": 500,
            "extendOutputFunction": """($) => { return {
                "scrapedType": undefined, 
                "reviews":undefined, 
                "Yield": undefined,  
                "nutritionFacts":undefined, 
                "rating": undefined,
                "author": undefined, 
                "breadcrumbs": undefined   
            } }""",
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
        all_recipes = all_recipes + recipes

        file_name = CUISINE[index] + '.json'
        file_dir = os.path.join(save_path, file_name)
        with open(file_dir, 'w') as f:
            json.dump(all_recipes, f, indent=4, ensure_ascii=False)
    
    
Recipe_Crawler()