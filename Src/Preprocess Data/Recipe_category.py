import pandas as pd
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from nltk.stem import WordNetLemmatizer
import os

mylist =['fish', 'goat', 'chicken','beef','pork','prawn','egg','Katsuobushi',
         'mackrel','fillet','lamb','steak','salmon','shrimp','bacon','ham',
         'turkey','duck','seafood','squid','bread','milk','butter','whipping',
         'cream','cheese','yogurt','sausage']

def Read_Directory(directory):
    database = []
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        data = []
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding = 'utf-8') as file:
                data = json.load(file)
                database.extend(data)

        elif os.path.isdir(file_path):
            database.extend(Read_Directory(file_path))
    
    return database

#Load recipe data
data_dir = os.path.join(os.getcwd(), 'Data', 'Preprocess Data', 'Recipes')
db = Read_Directory(data_dir)

df = []
for i, recipe in enumerate(db):
    ings = ""
    for ing in recipe['ingredients']:
        ings += "," + str(ing['unit']) + ing['name'] + str(ing['prepare_type'])
    ings = WordNetLemmatizer().lemmatize(re.sub('[^A-Za-z]', ' ', ings))
    if any(item in ings for item in mylist):
        if recipe['tags'] == "":
            recipe['tags'] = ['non-vegan']
        else:
            recipe['tags'].append('non-vegan')
    else:
        if recipe['tags'] == "":
            recipe['tags'] = ['vegan']
        else:
            recipe['tags'].append('vegan')


data_dir = os.path.join(os.getcwd(), 'Data', 'Database', 'Recipes', 'Recipe.json')
with open(data_dir, "r", encoding = 'utf-8') as file:
    recipes = json.load(file)

for recipe in recipes:
    found = next((item for item in db if item["url"] == recipe['url']), None)
    recipe['tags'] = found['tags']


data_dir = os.path.join(os.getcwd(), 'Data', 'Database', 'Recipes', 'Category_Recipes.json')
with open(data_dir, "w") as file:
    json.dump(recipes, file, indent=4)