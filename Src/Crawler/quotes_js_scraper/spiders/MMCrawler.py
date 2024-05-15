import json
import os
import math
import scrapy
from quotes_js_scraper.items import MMItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode
import requests

class MMCrawlerSpider(scrapy.Spider):
    name = 'MMCrawler'
    
    def __init__(self, number_products_laptop_fpt=3, *args, **kwargs):
        super(MMCrawlerSpider, self).__init__(*args, **kwargs)
        self.number_products_laptop_fpt = number_products_laptop_fpt

    def start_requests(self):
        start_urls = ["https://online.mmvietnam.com/danh-muc/mm-an-phu/thuc-pham-tuoi-song/", "https://online.mmvietnam.com/danh-muc/mm-an-phu/do-an-che-bien/", "https://online.mmvietnam.com/danh-muc/mm-an-phu/bo-trung-sua/", "https://online.mmvietnam.com/danh-muc/mm-an-phu/thuc-pham-dong-lanh/", "https://online.mmvietnam.com/danh-muc/mm-an-phu/dau-an-gia-vi-nuoc-cham/", "https://online.mmvietnam.com/danh-muc/mm-an-phu/do-hop-do-kho/", "https://online.mmvietnam.com/danh-muc/mm-an-phu/do-uong-cac-loai/", "https://online.mmvietnam.com/danh-muc/mm-an-phu/banh-keo-cac-loai/"]
        page_numbers = [62, 33, 43, 25, 67, 76, 92, 76]
        
        # start_url = start_urls[0] + f"page/{0 + 1}/"
        # yield SeleniumRequest(url=start_url, callback=self.parse_search_pages, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'product')), meta={'url_cat': start_urls[0], 'page': 0 + 1})
        for i in range(len(start_urls)):
            for p in range(page_numbers[i]):
                start_url = start_urls[i] + f"page/{p + 1}/"
                yield SeleniumRequest(url=start_url, callback=self.parse_search_pages, wait_time=10, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'product')), meta={'url_cat': start_urls[i], 'page': p + 1})

    def parse_search_pages(self, response):
        products  = response.css('.product')
        product_item = MMItem()
        original_category = response.meta['url_cat']
        category = ' '.join(original_category.split('/')[-2].split('-')).lower()

        product_all = []
        for product in products:
            try:
                description = product.css('.block-title a::text').get().split(", ")
                product_item['name'] = description[0]
                product_item['price'] = product.css('div.display-price .woocommerce-Price-amount bdi::text').get()
                product_item['unit'] = product.css('div.display-price .uom::text').get()
                product_item['url'] = product.css('.block-title a').attrib["href"]
                product_item['category'] = category
                product_item['image'] = product.css('a.product-image img').attrib["src"]
                if len(description) > 1:
                    product_item['quantity'] = description[1]
                product_item['domain_url'] = "https://online.mmvietnam.com/"

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
            except KeyError:
                continue
        
        filename = f"Data MM 1/{category}/page {response.meta['page']}.json"

        data_directory = "Data MM 1"
        category_directory = os.path.join(data_directory, category)
        if not os.path.exists(category_directory):
            os.makedirs(category_directory)

        with open(filename, 'w', encoding = 'utf-8') as f:
            json.dump(product_all, f, indent = 4, ensure_ascii = False) 