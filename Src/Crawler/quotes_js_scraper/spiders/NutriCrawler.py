import json
import os
import math
import scrapy
from quotes_js_scraper.items import NutriItem, VitaItem, MineItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode
import requests

class NutriCrawlerSpider(scrapy.Spider):
    name = 'NutriCrawler'
    
    def __init__(self, number_products_laptop_fpt=3, *args, **kwargs):
        super(NutriCrawlerSpider, self).__init__(*args, **kwargs)
        self.number_products_laptop_fpt = number_products_laptop_fpt

    def start_requests(self):
        # start_url = 'https://www.nutritiontable.com/nutritions/'
        # start_url = 'https://www.nutritiontable.com/nutritions/vitamins/'
        start_url = 'https://www.nutritiontable.com/nutritions/minerals/'

        cnt = 0
        for c in range(ord('A'), ord('Z')+1):
            next_url = start_url + chr(c) + '/'

            if chr(c) == 'A':
                next_url = start_url
            
            # if chr(c) != 'F':
            #     continue

            if chr(c) == 'Z':
                # yield SeleniumRequest(url=next_url, callback=self.parse_search_nutritions, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'vwRow')), meta={'url': next_url, 'nutri': chr(c)})
                # yield SeleniumRequest(url=next_url, callback=self.parse_search_vitamins, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'vwRow')), meta={'url': next_url, 'nutri': chr(c)})
                yield SeleniumRequest(url=next_url, callback=self.parse_search_minerals, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'vwRow')), meta={'url': next_url, 'nutri': chr(c)})
            elif chr(c) != 'X' and chr(c) != 'U':
                # yield SeleniumRequest(url=next_url, callback=self.parse_search_nutritions, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'vwRow1')), meta={'url': next_url, 'nutri': chr(c)})
                # yield SeleniumRequest(url=next_url, callback=self.parse_search_vitamins, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'vwRow1')), meta={'url': next_url, 'nutri': chr(c)})
                yield SeleniumRequest(url=next_url, callback=self.parse_search_minerals, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'vwRow1')), meta={'url': next_url, 'nutri': chr(c)})
            
            # cnt += 1
            # if cnt == 1:
            #     break

    def parse_search_nutritions(self, response):
        products = response.css('.vwRow, .vwRow1')

        product_item = NutriItem()        
        product_all = []
        for product in products:
            try:
                product_item['name'] = product.css('.prodNameLink::text').get()
                product_item['energy_kcal'] = product.css('div[title="Kcal (kcal)"] span::text').get()
                product_item['energy_kj'] = product.css('div[title="Kjoule (kJ)"] span::text').get()
                product_item['water_g'] = product.css('div[title="Water (g)"] span::text').get()
                product_item['protein_g'] = product.css('div[title="Protein (g)"] span::text').get()
                product_item['carbohydrates_g'] = product.css('div[title="Carbohydrates (g)"] span::text').get()
                product_item['sugars_g'] = product.css('div[title="Sugars (g)"] span::text').get()
                product_item['fat_g'] = product.css('div[title="Fat (g)"] span::text').get()
                product_item['saturated_fat_g'] = product.css('div[title="Saturated Fat (g)"] span::text').get()
                product_item['monounsaturated_fat_g'] = product.css('div[title="Monounsaturated fat (g)"] span::text').get()
                product_item['polyunsaturated_fat_g'] = product.css('div[title="Polyunsaturated fat (g)"] span::text').get()
                product_item['cholesterol_mg'] = product.css('div[title="Cholesterol (mg)"] span::text').get()
                product_item['dietary_fiber_g'] = product.css('div[title="Fiber (g)"] span::text').get()
                product_item['emotional_value'] = product.css('[id$="lblFeeling"]::text').get()
                product_item['health_value'] = product.css('[id$="lblHealty"]::text').get()
                product_item['url'] = "https://www.nutritiontable.com" + product.css('.prodNameLink').attrib["href"]

                data = {
                    'name': product_item['name'],
                    'energy_kcal': product_item['energy_kcal'],
                    'energy_kj': product_item['energy_kj'],
                    'water_g': product_item['water_g'],
                    'protein_g': product_item['protein_g'],
                    'carbohydrates_g': product_item['carbohydrates_g'],
                    'sugars_g': product_item['sugars_g'],
                    'fat_g': product_item['fat_g'],
                    'saturated_fat_g': product_item['saturated_fat_g'],
                    'monounsaturated_fat_g': product_item['monounsaturated_fat_g'],
                    'polyunsaturated_fat_g': product_item['polyunsaturated_fat_g'],
                    'cholesterol_mg': product_item['cholesterol_mg'],
                    'dietary_fiber_g': product_item['dietary_fiber_g'],
                    'emotional_value': product_item['emotional_value'],
                    'health_value': product_item['health_value'],
                    'url': product_item['url'],
                }

                # print(data)
                product_all.append(data)
            except KeyError:
                continue
        
        # print(product_all)
        filename = f"Data Nutri 2/{response.meta['nutri']}.json"
        with open(filename, 'w', encoding = 'utf-8') as f:
            json.dump(product_all, f, indent = 4, ensure_ascii = False) 
    
    def parse_search_vitamins(self, response):
        products = response.css('.vwRow, .vwRow1')
        print(len(products))
        product_item = VitaItem()        
        product_all = []
        for product in products:
            try:
                product_item['name'] = product.css('.prodNameLink::text').get()
                product_item['vitamin_A_mg'] = product.css('div[title="Vitamin A (mg)"] span::text').get()
                product_item['vitamin_B1_mg'] = product.css('div[title="Vitamin B1 (mg)"] span::text').get()
                product_item['vitamin_B2_mg'] = product.css('div[title="Vitamin B2 (mg)"] span::text').get()
                product_item['vitamin_B3_mg'] = product.css('div[title="Vitamin B3 (mg)"] span::text').get()
                product_item['vitamin_B6_mg'] = product.css('div[title="Vitamin B6 (mg)"] span::text').get()
                product_item['vitamin_B11_microgram'] = product.css('[id$="lblVitB11"]::text').get()
                product_item['vitamin_B12_microgram'] = product.css('[id$="lblVitB12"]::text').get()
                product_item['vitamin_C_mg'] = product.css('div[title="Vitamin C (mg)"] span::text').get()
                product_item['vitamin_D_microgram'] = product.css('[id$="lblVitD"]::text').get()
                product_item['vitamin_E_mg'] = product.css('div[title="Vitamin E (mg)"] span::text').get()
                product_item['vitamin_K_microgram'] = product.css('[id$="lblVitK"]::text').get()
                product_item['emotional_value'] = product.css('[id$="lblVitB11"]::text').get()
                product_item['health_value'] = product.css('[id$="lblHealty"]::text').get()
                product_item['url'] = "https://www.nutritiontable.com" + product.css('.prodNameLink').attrib["href"]

                data = {
                    'name': product_item['name'],
                    'vitamin_A_mg': product_item['vitamin_A_mg'],
                    'vitamin_B1_mg': product_item['vitamin_B1_mg'],
                    'vitamin_B2_mg': product_item['vitamin_B2_mg'],
                    'vitamin_B3_mg': product_item['vitamin_B3_mg'],
                    'vitamin_B6_mg': product_item['vitamin_B6_mg'],
                    'vitamin_B11_microgram': product_item['vitamin_B11_microgram'],
                    'vitamin_B12_microgram': product_item['vitamin_B12_microgram'],
                    'vitamin_C_mg': product_item['vitamin_C_mg'],
                    'vitamin_D_microgram': product_item['vitamin_D_microgram'],
                    'vitamin_E_mg': product_item['vitamin_E_mg'],
                    'vitamin_K_microgram': product_item['vitamin_K_microgram'],
                    'emotional_value': product_item['emotional_value'],
                    'health_value': product_item['health_value'],
                    'url': product_item['url'],
                }

                product_all.append(data)
            except KeyError:
                continue
        
        # print(product_all)
        filename = f"Data Nutri 2/{response.meta['nutri']}_vitamins.json"
        with open(filename, 'w', encoding = 'utf-8') as f:
            json.dump(product_all, f, indent = 4, ensure_ascii = False) 

    def parse_search_minerals(self, response):
        products = response.css('.vwRow, .vwRow1')

        product_item = MineItem()        
        product_all = []
        for product in products:
            try:
                product_item['name'] = product.css('.prodNameLink::text').get()
                product_item['sodium_mg'] = product.css('div[title="Sodium (mg)"] span::text').get()
                product_item['potassium_mg'] = product.css('div[title="Potassium (mg)"] span::text').get()
                product_item['calcium_mg'] = product.css('div[title="Calcium (mg)"] span::text').get()
                product_item['phosphor_mg'] = product.css('div[title="Phosphor (mg)"] span::text').get()
                product_item['iron_mg'] = product.css('div[title="Iron (mg)"] span::text').get()
                product_item['magnesium_mg'] = product.css('div[title="Magnesium (mg)"] span::text').get()
                product_item['copper_mg'] = product.css('div[title="Copper (mg)"] span::text').get()
                product_item['zinc_mg'] = product.css('div[title="Zinc (mg)"] span::text').get()
                product_item['selenium_microgram'] = product.css('[id$="lblMinSe"]::text').get()
                product_item['iodine_microgram'] = product.css('[id$="lblMinI"]::text').get()
                product_item['manganese_microgram'] = product.css('[id$="lblMinMn"]::text').get()
                product_item['emotional_value'] = product.css('[id$="lblFeeling"]::text').get()
                product_item['health_value'] = product.css('[id$="lblHealty"]::text').get()
                product_item['url'] = "https://www.nutritiontable.com" + product.css('.prodNameLink').attrib["href"]

                data = {
                    'name': product_item['name'],
                    'sodium_mg': product_item['sodium_mg'],
                    'potassium_mg': product_item['potassium_mg'],
                    'calcium_mg': product_item['calcium_mg'],
                    'phosphor_mg': product_item['phosphor_mg'],
                    'iron_mg': product_item['iron_mg'],
                    'magnesium_mg': product_item['magnesium_mg'],
                    'copper_mg': product_item['copper_mg'],
                    'zinc_mg': product_item['zinc_mg'],
                    'selenium_microgram': product_item['selenium_microgram'],
                    'iodine_microgram': product_item['iodine_microgram'],
                    'manganese_microgram': product_item['manganese_microgram'],
                    'emotional_value': product_item['emotional_value'],
                    'health_value': product_item['health_value'],
                    'url': product_item['url'],
                }

                # print(data)
                product_all.append(data)
            except KeyError:
                continue
        
        # print(product_all)
        filename = f"Data Nutri 2/{response.meta['nutri']}_minerals.json"
        with open(filename, 'w', encoding = 'utf-8') as f:
            json.dump(product_all, f, indent = 4, ensure_ascii = False) 