# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class BHXItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    quantity = scrapy.Field()
    domain_url = scrapy.Field()
    
class MMItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    quantity = scrapy.Field()
    domain_url = scrapy.Field()

class WSSItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    quantity = scrapy.Field()
    domain_url = scrapy.Field()

class NutriItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    energy_kcal = scrapy.Field()
    energy_kj = scrapy.Field()
    water_g = scrapy.Field()
    protein_g = scrapy.Field()
    carbohydrates_g = scrapy.Field()
    sugars_g = scrapy.Field()
    fat_g = scrapy.Field()
    saturated_fat_g = scrapy.Field()
    monounsaturated_fat_g = scrapy.Field()
    polyunsaturated_fat_g = scrapy.Field()
    cholesterol_mg = scrapy.Field()
    dietary_fiber_g = scrapy.Field()
    emotional_value = scrapy.Field()
    health_value = scrapy.Field()
    url = scrapy.Field()

class VitaItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    vitamin_A_mg = scrapy.Field()
    vitamin_B1_mg = scrapy.Field()
    vitamin_B2_mg = scrapy.Field()
    vitamin_B3_mg = scrapy.Field()
    vitamin_B6_mg = scrapy.Field()
    vitamin_B11_microgram = scrapy.Field()
    vitamin_B12_microgram = scrapy.Field()
    vitamin_C_mg = scrapy.Field()
    vitamin_D_microgram = scrapy.Field()
    vitamin_E_mg = scrapy.Field()
    vitamin_K_microgram = scrapy.Field()
    emotional_value = scrapy.Field()
    health_value = scrapy.Field()
    url = scrapy.Field()

class MineItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    sodium_mg = scrapy.Field()
    potassium_mg = scrapy.Field()
    calcium_mg = scrapy.Field()
    phosphor_mg = scrapy.Field()
    iron_mg = scrapy.Field()
    magnesium_mg = scrapy.Field()
    copper_mg = scrapy.Field()
    zinc_mg = scrapy.Field()
    selenium_microgram = scrapy.Field()
    iodine_microgram = scrapy.Field()
    manganese_microgram = scrapy.Field()
    emotional_value = scrapy.Field()
    health_value = scrapy.Field()
    url = scrapy.Field()
