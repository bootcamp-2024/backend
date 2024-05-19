import pandas as pd
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from nltk.stem import WordNetLemmatizer
import os


#Removing the stop words from ingredients and vectorizing
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 1), analyzer='word', token_pattern=r'\w+')

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
    ings = []
    for ing in recipe['ingredients']:
        ings += "," + ing['name']
    recipe['ing'] = ings
    df.append(recipe)

df_test = pd.DataFrame(df)

#Lemmatizing the ingredients column and vectorizing
df_test['ingredients_mod'] = [WordNetLemmatizer().lemmatize(re.sub('[^A-Za-z]', ' ', line)) for line in df_test["ing"]]       
test_tfidf = vectorizer.transform(df_test['ingredients_mod'])

#Load model
filename = os.path.join(os.getcwd(), 'Src', 'Cuisine_Classifier', 'Model', 'model.pkl')
with open(filename,'rb') as f:
    lsvc_veg = pickle.load(f)

Type_pred = lsvc_veg.predict(test_tfidf)
df_test['tags'] = df_test['tags'].append(Type_pred)

data_dir = os.path.join(os.getcwd(), 'Data', 'Database', 'Recipes', 'Vietnamese_Recipes.json')
with open(data_dir, "w") as file:
    json.dump(df_test, file)