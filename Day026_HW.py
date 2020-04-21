# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 02:46:43 2020

@author: camer
"""

from ptt.items import PttItem
import scrapy
import time
from bs4 import BeautifulSoup

class PttSpider(scrapy.Spider):
    name = 'ptt'
    allowed_domains = ['ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Gossiping/index.html']
    
    def parse(self, response):
        for i in range(100):
            time.sleep(1)
            url = 'https://www.ptt.cc/bbs/Gossiping/index' + str(39701-i) + '.html'
            yield scrapy.Request(url, cookies={'over18':'1'}, callback=self.parse_article)
        
    def parse_article(self, response):
        item = PttItem()
        res = BeautifulSoup(response.body)
        target = res.select('div .r-ent')
        
        for j in target:
            try:
                item['title'] = j.select('div .title')[0].text.strip(' \t\n\r')
                item['author'] = j.select('div .author')[0].text.strip(' \t\n\r')
                item['date'] = j.select('div .date')[0].text.strip(' \t\n\r')
                try:
                    item['push'] = j.select('span')[0].text.strip(' \t\n\r')
                except:
                    item['push'] ='0'
                item['url'] = j.select('div .title')[0].find('a')['href']
            
                yield item
            except IndexError:
                pass
            
            continue
            