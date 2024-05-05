import json
import os
import math
import scrapy
from quotes_js_scraper.items import BHXItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode
import requests

class BHXCrawlerSpider(scrapy.Spider):
    name = 'BHXCrawler'
    
    def __init__(self, number_products_laptop_fpt=3, *args, **kwargs):
        super(BHXCrawlerSpider, self).__init__(*args, **kwargs)
        self.number_products_laptop_fpt = number_products_laptop_fpt

    def start_requests(self):
        start_url = 'https://www.bachhoaxanh.com/sitemapnew/sitemap-cate'
        yield SeleniumRequest(url=start_url, callback=self.parse_search_links, wait_time=1)

    def parse_search_links(self, response):
        links = response.css('.folder > div.opened > div:nth-child(2) > span:nth-child(2)::text').getall()
        # yield SeleniumRequest(url=links[0], callback=self.parse_search_pages, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'box_product')), meta={'url': links[0]})
        for link in links:
            yield SeleniumRequest(url=link, callback=self.parse_search_pages, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'box_product')), meta={'url': link})

    def parse_search_pages(self, response):
        products  = response.css('.box_product')
        product_item = BHXItem()
        original_category = response.meta['url']
        category = ' '.join(original_category.split('/')[-1].split('-')).lower()
        
        product_all = []
        for product in products:
            try:
                product_item['name'] = product.css('a.relative.w-full').attrib["title"]
                
                product_item['category'] = category
                
                product_item['url'] = 'https://www.bachhoaxanh.com' + product.css('a.relative.w-full').attrib["href"]

                original_img = product.css('a.relative.w-full img').attrib["src"]
                product_item['image'] = 'https' + original_img.split('https')[2]

                original_price = product.css('.product_price::text').get()
                if original_price is not None:
                    product_item['price'] = original_price.replace('.', '').replace('₫', '').replace(',', '').strip()
                else:
                    product_item['price'] = ''
                
                original_quantity = product.css('.product_price div::text').get()
                if original_quantity is not None:
                    temp = original_quantity[1:].split(' ')
                    if len(temp) > 1:
                        product_item['unit'] = temp[0]
                        product_item['quantity'] = temp[1]
                    else:
                        product_item['quantity'] = temp[0]
                        product_item['unit'] = ''
                else:
                    product_item['quantity'] = ''
                    product_item['unit'] = ''

                product_item['domain_url'] = 'https://www.bachhoaxanh.com'

                data = {
                    'name': product_item['name'],
                    'category': product_item['category'],
                    'url': product_item['url'],
                    'image': product_item['image'],
                    'price': product_item['price'],
                    'quantity': product_item['quantity'],
                    'unit': product_item['unit'],
                    'domain_url': product_item['domain_url'],
                }

                product_all.append(data)
            except KeyError:
                continue
        
        # print(product_all)
        filename = f"Data BHX 3/BHX_{category}.json"
        with open(filename, 'w', encoding = 'utf-8') as f:
            json.dump(product_all, f, indent = 4, ensure_ascii = False) 