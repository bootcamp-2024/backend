import json
import os
import math
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode
import requests

class RecipeCrawlerSpider(scrapy.Spider):
    name = 'RecipeCrawler'
    
    def __init__(self, number_products_laptop_fpt=3, *args, **kwargs):
        super(RecipeCrawlerSpider, self).__init__(*args, **kwargs)
        self.number_products_laptop_fpt = number_products_laptop_fpt

    def start_requests(self):
        start_urls = ['https://www.allrecipes.com/recipes/695/world-cuisine/asian/chinese/', 'https://www.allrecipes.com/recipes/16100/world-cuisine/asian/bangladeshi/', 'https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/', 'https://www.allrecipes.com/recipes/15974/world-cuisine/asian/pakistani/', 'https://www.allrecipes.com/recipes/696/world-cuisine/asian/filipino/', 'https://www.allrecipes.com/recipes/698/world-cuisine/asian/indonesian/', 'https://www.allrecipes.com/recipes/699/world-cuisine/asian/japanese/', 'https://www.allrecipes.com/recipes/700/world-cuisine/asian/korean/', 'https://www.allrecipes.com/recipes/701/world-cuisine/asian/malaysian/', 'https://www.allrecipes.com/recipes/702/world-cuisine/asian/thai/', 'https://www.allrecipes.com/recipes/703/world-cuisine/asian/vietnamese/', 'https://www.allrecipes.com/recipes/15937/world-cuisine/middle-eastern/persian/'] 
        
        # cnt = 0
        for url in start_urls:
            nation = url.split('/')[-2]

            yield SeleniumRequest(url=url, callback=self.parse_search_links, wait_time=10, meta={'path': [nation]})
            # yield SeleniumRequest(url=url, callback=self.parse_search_links, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'mntl-taxonomysc-article-list-group')), meta={'path': [nation]})

            # cnt += 1
            # if cnt == 1:
            #     break

    def parse_search_links(self, response):
        links = response.css('.mntl-taxonomy-nodes__item a')
        
        if len(links) == 0:
            products = json.loads(response.css('.allrecipes-schema::text').get())[0]
            link_products = products['itemListElement']
            # products = response.css('.mntl-taxonomysc-article-list-group .mntl-card-list-items')

            path = response.meta['path']
            base_folder = "Data Recipe 3"

            for folder_name in path:
                folder_path = os.path.join(base_folder, folder_name)
                
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                base_folder = folder_path
            
            filename = os.path.join(base_folder, "data.json")
            with open(filename, "w") as f:
                pass

            # cnt = 0
            for p in link_products:
                link_product = p['url']
                # print(link_product)
                # print(response.meta['path'])
                
                yield SeleniumRequest(url=link_product, callback=self.parse_search_products, wait_time=10, wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '#allrecipes-schema_1-0')), meta={'url': link_product, 'file name': filename, 'path': response.meta['path']})

                # cnt += 1
                # if cnt == 1:
                #     break
        else:
            # cnt = 0
            for _ in links:
                link = _.attrib["href"]            
                path = response.meta['path'].copy()
                path.append(_.css('span::text').get())

                yield SeleniumRequest(url=link, callback=self.parse_search_links, wait_time=10, meta={'path': path})
                # yield SeleniumRequest(url=link, callback=self.parse_search_links, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'mntl-taxonomysc-article-list-group')), meta={'path': path})

                # cnt += 1
                # if cnt == 1:
                #     break

    def parse_search_products(self, response):
        product = json.loads(response.css('.allrecipes-schema::text').get())[0]

        filename = response.meta['file name']
        with open(filename, 'r', encoding = 'utf-8') as f:
            try:
                product_all = json.load(f)
            except json.JSONDecodeError as e:
                product_all = []

        try:
            nutrition = product['nutrition']
            if "@type" in nutrition:
                del nutrition["@type"]

            instructions = product['recipeInstructions']
            for step in instructions:
                if "@type" in step:
                    del step["@type"]
                if "image" in step:
                    del step["image"]
            
            video = product['video']
            if "@type" in video:
                del video["@type"]
            if "thumbnailUrl" in video:
                del video["thumbnailUrl"]
            if "uploadDate" in video:
                del video["uploadDate"]

            ingredients = response.css('.mntl-structured-ingredients__list-item')
            ingredients_list = []
            for i in ingredients:
                ingredient = {
                    'quantity': i.css('[data-ingredient-quantity]::text').get(),
                    'unit': i.css('[data-ingredient-unit]::text').get(),
                    'name': i.css('[data-ingredient-name]::text').get(),
                }
                ingredients_list.append(ingredient)

            data = {
                'name': product['name'],
                'cook_time': product['cookTime'],
                'prep_time': product['prepTime'],
                'total_time': product['totalTime'],
                'nutrition': nutrition,
                'description': product['description'],
                'cuisine': response.meta['path'][0],
                'category': product['recipeCategory'][0],
                'ingredient': ingredients_list,
                'instructions': instructions,
                'image': product['image']['url'],
                'video': video,
                'url': response.meta['url'],
            }

            # print(data)
            product_all.append(data)
        except KeyError:
            return
        
        with open(filename, 'w', encoding = 'utf-8') as f:
            json.dump(product_all, f, indent = 4, ensure_ascii = False)
