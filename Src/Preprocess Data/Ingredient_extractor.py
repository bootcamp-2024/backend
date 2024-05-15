import json
import os
from pattern.en import singularize
import numpy as np
from math import floor
from googletrans import Translator
import time

def Recipe_Translator(recipes):
    translator = Translator()
    total_len = len(recipes)
    for index, recipe in enumerate(recipes):
        recipe['name'] = translator.translate(recipe['name'], dest='vi').text
        recipe['description'] = translator.translate(recipe['description'], dest='vi').text
        instructions = []
        recipe_instruction = recipe.get("instructions")
        if recipe_instruction is not None:
            for instruction in recipe["instructions"]:
                instructions.append(translator.translate(instruction, dest='vi').text)
                time.sleep(0.2)
            recipe["instructions"] = instructions
        for ingredient in recipe['ingredients']:
            if ingredient['unit'] is not None and ingredient['unit'] != '':
                ingredient['unit'] = translator.translate(ingredient['unit'], dest='vi').text
            if ingredient['prepare_type'] != "":
                ingredient['prepare_type'] = translator.translate(ingredient['prepare_type'], dest='vi').text
        print(f"\rFinish {(index + 1) / total_len * 100:.4f}% work of recipe translation", end=" ")
        time.sleep(1)
    print()
    return recipes

def Ingredient_Translator(ingredients):
    translator = Translator()

    total_len = len(ingredients)
    for index, ingredient in enumerate(ingredients):
        ingredient['name'] = translator.translate(ingredient['name'], dest='vi').text
        print(f"\rFinish {(index + 1)/ total_len * 100:.4f}% work of ingredient translation", end=" ")

    print()
    return ingredients

def jaro_distance(text_1, text_2):
	
	# If the s are equal
	if (text_1 == text_2):
		return 1.0

	# Length of two s
	len1 = len(text_1)
	len2 = len(text_2)

	# Maximum distance upto which matching
	# is allowed
	max_dist = floor(max(len1, len2) / 2) - 1

	# Count of matches
	match = 0

	# Hash for matches
	hash_text_1 = [0] * len(text_1)
	hash_text_2 = [0] * len(text_2)

	# Traverse through the first
	for i in range(len1):

		# Check if there is any matches
		for j in range(max(0, i - max_dist), 
					min(len2, i + max_dist + 1)):
			
			# If there is a match
			if (text_1[i] == text_2[j] and hash_text_2[j] == 0):
				hash_text_1[i] = 1
				hash_text_2[j] = 1
				match += 1
				break

	# If there is no match
	if (match == 0):
		return 0.0

	# Number of transpositions
	t = 0
	point = 0

	# Count number of occurrences
	# where two characters match but
	# there is a third matched character
	# in between the indices
	for i in range(len1):
		if (hash_text_1[i]):

			# Find the next matched character
			# in second
			while (hash_text_2[point] == 0):
				point += 1

			if (text_1[i] != text_2[point]):
				t += 1
			point += 1
	t = t//2

	# Return the Jaro Similarity
	return (match/ len1 + match / len2 +
			(match - t) / match)/ 3.0

def longestCommonSubsequence(text_1, text_2):
    n = len(text_1)
    m = len(text_2)

    # Initializing two lists of size m
    prev = [0] * (m + 1)
    cur = [0] * (m + 1)

    for idx1 in range(1, n + 1):
        for idx2 in range(1, m + 1):
            # If characters are matching
            if text_1[idx1 - 1] == text_2[idx2 - 1]:
                cur[idx2] = 1 + prev[idx2 - 1]
            else:
                # If characters are not matching
                cur[idx2] = max(cur[idx2 - 1], prev[idx2])

        prev = cur.copy()

    return cur[m]/ min(m, n)

def Smith_Waterman(seq1, seq2, insertion_penalty=-1, deletion_penalty=-1, mismatch_penalty=-1, match_score=2):
    # Initialize the scoring matrix and other variables
    a, b = len(seq1), len(seq2)
    p = np.zeros((a + 1, b + 1))

    # Calculate scores for each cell
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            vertical_score = p[i - 1][j] + deletion_penalty
            horizontal_score = p[i][j - 1] + insertion_penalty
            if seq1[i - 1] == seq2[j - 1]:
                diagonal_score = p[i - 1][j - 1] + match_score
            else:
                diagonal_score = p[i - 1][j - 1] + mismatch_penalty
            p[i][j] = max(0, vertical_score, horizontal_score, diagonal_score)

    # Find the maximum score in the matrix (local alignment score)
    max_score = np.max(p)

    return max_score

			
def Calculate_Similarity(text_1, text_2):
    LCS = longestCommonSubsequence(text_1, text_2)
    jaro = jaro_distance(text_1, text_2)
    smith = Smith_Waterman(text_1, text_2)
    similarity_score = LCS * 0.4 + jaro * 0.2 + smith * 0.4
	
    return similarity_score


def Mapping_Data(ingredient_data, mapping_data, mapping_name):
	combined_data = []
		
	total_len = len(ingredient_data)
	for index, ingredient in enumerate(ingredient_data):
		max_similarity = 0
		max_mapping = {}
		for mapping in mapping_data:
			if ingredient['name'] != "":
				similarity = Calculate_Similarity(ingredient['name'], mapping['name'])
				if max_similarity < similarity and similarity > 0.99:
					max_similarity = max(similarity, max_similarity)
					max_mapping = mapping.copy()
		if mapping_name == 'nutritions':
			ingredient[mapping_name] = max_mapping
			combined_data.append(ingredient)
		else:
			if mapping_name in ingredient:
				ingredient[mapping_name].append(max_mapping)
			else:
				ingredient[mapping_name] = [max_mapping]
			combined_data.append(ingredient)
		print(f"\rFinish {(index + 1)/ total_len * 100:.4f}% work of mapping ingrdient and {mapping_name}", end=" ")
	
	print()
	return combined_data 

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


def Extract_Ingredient():
    data_dir = os.path.join(os.getcwd(), 'Data', 'Preprocess Data', 'Recipes')
    recipes = Read_Directory(data_dir)
    ingredients = []

    for recipe in recipes:
        for ingredient in recipe["ingredients"]:
            ingredients.append(ingredient['name'])
        
    idx = 0
    indexed_ingredients = []
    for ingredient in set(ingredients):
        if ingredient != '':
            ID = "ING" + str(idx)
            indexed_ingredient = {
                "_id": ID,
                "name": singularize(ingredient)
            }
            indexed_ingredients.append(indexed_ingredient)
            idx += 1
    
    return indexed_ingredients

def Find_Ingredient_ID(ingredient_name, ingredient_data):
    for ingredient in ingredient_data:
        if singularize(ingredient['name']) == ingredient_name:
            return ingredient['_id']

def Recipe_ID_Replacement(ingredients):
    data_dir = os.path.join(os.getcwd(), 'Data', 'Preprocess Data', 'Recipes')
    recipes = Read_Directory(data_dir)
    
    total_len = len(recipes)
    for index, recipe in enumerate(recipes):
        for ingredient in recipe['ingredients']:
            ingredient['ingredient_id'] = Find_Ingredient_ID(ingredient['name'], ingredients)
            del ingredient['name']
        print(f"\rFinish {(index +1)/ total_len * 100:.4f}% work of replace recipe ingredient ID", end=" ")
    
    print()
    # recipes = Recipe_Translator(recipes)
    data_dir = os.path.join(os.getcwd(), 'Data', 'Database', 'Recipes', 'Recipes.json')
    with open(data_dir, "w") as file:
        json.dump(recipes, file, indent=4)


def Nutrition_Joining(ingredients):
    data_dir = os.path.join(os.getcwd(), 'Data', 'Crawled', 'Nutrition')
    nutrition_data = Read_Directory(data_dir)

    combined_data = Mapping_Data(ingredients, nutrition_data, 'nutritions')
    for data_point in combined_data[:1]:
        data_point['name'] = data_point['nutritions']['name']
        del data_point['nutritions']['name']

    return combined_data

def Price_Joining(ingredients):
    domains = ['Data BHX 3', 'Data MM 1', 'Data WSS 1']
    combined_data = ingredients
    for domain in domains:
        data_dir = os.path.join(os.getcwd(), 'Data', 'Crawled', 'Price', domain)
        price_data = Read_Directory(data_dir)
        combined_data = Mapping_Data(combined_data, price_data, 'unit_price')

        data_dir = os.path.join(os.getcwd(), 'Data', 'Database', 'Ingredient', 'Ingredient.json')
        with open(data_dir, "w") as file:
            json.dump(ingredients, file, indent=4)

    return combined_data

ingredients = Extract_Ingredient()
Recipe_ID_Replacement(ingredients)

# ingredients = Nutrition_Joining(ingredients)
# data_dir = os.path.join(os.getcwd(), 'Data', 'Database', 'Ingredient', 'Ingredient.json')
# with open(data_dir, "w") as file:
#     json.dump(ingredients, file, indent=4)

# ingredients = Ingredient_Translator(ingredients)
# with open(data_dir, "w") as file:
#     json.dump(ingredients, file, indent=4)
    
# ingredients = Price_Joining(ingredients)

# with open(data_dir, "w") as file:
#     json.dump(ingredients, file, indent=4)
