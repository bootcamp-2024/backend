import json
import os
import math
import scrapy
from quotes_js_scraper.items import WSSItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode
import requests

class WSSCrawlerSpider(scrapy.Spider):
    name = 'WSSCrawler'
    
    def __init__(self, number_products_laptop_fpt=3, *args, **kwargs):
        super(WSSCrawlerSpider, self).__init__(*args, **kwargs)
        self.number_products_laptop_fpt = number_products_laptop_fpt

    def start_requests(self):
        # for p in range(1, 31):
        for p in range(5, 31):
            start_url = f"https://websosanh.vn/thuc-pham-do-uong/cat-130?pi={p}.htm"
            yield SeleniumRequest(url=start_url, callback=self.parse_search_pages, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'product-single')), meta={'page': p})

    def parse_search_pages(self, response):
        products  = response.css('.product-single')

        filename = f"Data WSS 1/page {response.meta['page']}.json"
        with open(filename, 'w', encoding = 'utf-8') as f:
            pass
            
        for product in products:
            product_url = product.css('.product-single-name a').attrib["href"]

            if product_url.endswith("so-sanh.htm"):
                next_url = "https://websosanh.vn" + product_url
                yield SeleniumRequest(url=next_url, callback=self.parse_search_products, wait_time=10, wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, 'head script[type="application/ld+json"]')), meta={'page': response.meta['page'], 'url': next_url})
    
    def parse_search_products(self, response):
        product = json.loads(response.css('head script[type="application/ld+json"]::text').getall()[-1])

        product_item = WSSItem()
        product_all = []
        filename = f"Data WSS 1/page {response.meta['page']}.json"
        with open(filename, 'r', encoding = 'utf-8') as f:
            try:
                product_all = json.load(f)
            except json.JSONDecodeError as e:
                product_all = []

        for _ in range(len(product['offers']['offers'])):
            try:
                product_item['name'] = product['name']
                product_item['price'] = product['offers']['offers'][0]['price']                
                product_item['unit'] = ''
                product_item['url'] = product['offers']['offers'][0]['url']
                product_item['category'] = product['category']
                product_item['image'] = product['image']
                product_item['quantity'] = ''
                
                original_url = product['offers']['offers'][0]['name']
                product_item['domain_url'] = "https://" + original_url.split(' ')[-1]

                data = {
                        'name': product_item['name'],
                        'price': product_item['price'],
                        'unit': product_item['unit'],
                        'url': product_item['url'],
                        'category': product_item['category'],
                        'image': product_item['image'],
                        'quantity': product_item['quantity'],
                        'domain_url': product_item['domain_url'],
                    }

                product_all.append(data)
                print(data)
            except KeyError:
                continue
        
        with open(filename, 'w', encoding = 'utf-8') as f:
            json.dump(product_all, f, indent = 4, ensure_ascii = False)