# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class RatioItem(Item):
    key_text=Field();
    key_type=Field();
    value=Field();
    year=Field();
    symbol=Field();
    month=Field();
    
