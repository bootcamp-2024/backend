import json

for c in range(ord('A'), ord('Z')+1):
    if chr(c) == 'U' or chr(c) == 'X':
        continue

    # Đọc dữ liệu từ các tệp JSON
    with open(f'Data Nutri 2/{chr(c)}_minerals.json', 'r', encoding='utf-8') as f:
        minerals_data = json.load(f)

    with open(f'Data Nutri 2/{chr(c)}_vitamins.json', 'r', encoding='utf-8') as f:
        vitamins_data = json.load(f)

    with open(f'Data Nutri 2/{chr(c)}.json', 'r', encoding='utf-8') as f:
        nutrition_data = json.load(f)

    # Gộp thông tin từ các tệp JSON vào một danh sách
    combined_data = []

    for mineral_item in minerals_data:
        for vitamin_item in vitamins_data:
            if mineral_item["name"] == vitamin_item["name"]:
                for nutrition_item in nutrition_data:
                    if mineral_item["name"] == nutrition_item["name"]:
                        combined_item = {
                            "name": mineral_item["name"],
                            
                            "energy_kcal": nutrition_item["energy_kcal"],
                            "energy_kj": nutrition_item["energy_kj"],
                            "water_g": nutrition_item["water_g"],
                            "protein_g": nutrition_item["protein_g"],
                            "carbohydrates_g": nutrition_item["carbohydrates_g"],
                            "sugars_g": nutrition_item["sugars_g"],
                            "fat_g": nutrition_item["fat_g"],
                            "saturated_fat_g": nutrition_item["saturated_fat_g"],
                            "monounsaturated_fat_g": nutrition_item["monounsaturated_fat_g"],
                            "polyunsaturated_fat_g": nutrition_item["polyunsaturated_fat_g"],
                            "cholesterol_mg": nutrition_item["cholesterol_mg"],
                            "dietary_fiber_g": nutrition_item["dietary_fiber_g"],
                            "nutrition_emotional_value": nutrition_item["emotional_value"],
                            "nutrition_health_value": nutrition_item["health_value"],

                            "vitamin_A_mg": vitamin_item["vitamin_A_mg"],
                            "vitamin_B1_mg": vitamin_item["vitamin_B1_mg"],
                            "vitamin_B2_mg": vitamin_item["vitamin_B2_mg"],
                            "vitamin_B3_mg": vitamin_item["vitamin_B3_mg"],
                            "vitamin_B6_mg": vitamin_item["vitamin_B6_mg"],
                            "vitamin_B11_microgram": vitamin_item["vitamin_B11_microgram"],
                            "vitamin_B12_microgram": vitamin_item["vitamin_B12_microgram"],
                            "vitamin_C_mg": vitamin_item["vitamin_C_mg"],
                            "vitamin_D_microgram": vitamin_item["vitamin_D_microgram"],
                            "vitamin_E_mg": vitamin_item["vitamin_E_mg"],
                            "vitamin_K_microgram": vitamin_item["vitamin_K_microgram"],
                            "vitamin_emotional_value": vitamin_item["emotional_value"],
                            "vitamin_health_value": vitamin_item["health_value"],

                            "sodium_mg": mineral_item["sodium_mg"],
                            "potassium_mg": mineral_item["potassium_mg"],
                            "calcium_mg": mineral_item["calcium_mg"],
                            "phosphor_mg": mineral_item["phosphor_mg"],
                            "iron_mg": mineral_item["iron_mg"],
                            "magnesium_mg": mineral_item["magnesium_mg"],
                            "copper_mg": mineral_item["copper_mg"],
                            "zinc_mg": mineral_item["zinc_mg"],
                            "selenium_microgram": mineral_item["selenium_microgram"],
                            "iodine_microgram": mineral_item["iodine_microgram"],
                            "manganese_microgram": mineral_item["manganese_microgram"],
                            "mineral_emotional_value": mineral_item["emotional_value"],
                            "mineral_health_value": mineral_item["health_value"],
                            
                            "url": nutrition_item["url"]
                        }
                        combined_data.append(combined_item)
                        break

    # Lưu thông tin gộp vào một tệp JSON mới
    with open(f'Data Nutri 2/{chr(c)}_nutritions.json', 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, indent=4, ensure_ascii=False)

    print(f"Gộp thông tin {chr(c)} thành công!")
