#bookvalue xpath //*[@id="mktdet_2"]/div[1]/div[3]/div[2]/text()
#pe xpath //*[@id="mktdet_2"]/div[1]/div[2]/div[2]/text()
#pc //*[@id="mktdet_2"]/div[2]/div[2]/div[2]/text()
#industry_pe //*[@id="mktdet_2"]/div[1]/div[6]/div[2]/text()
#nse_price //*[@id="Nse_Prc_tick"]/strong/text()
#bse_price //*[@id="Bse_Prc_tick"]/strong/text()
#sector //*[@id="nChrtPrc"]/div[4]/div[1]/a/text()
#52wlow //*[@id="n_52low"]/span/text()
#52whigh //*[@id="n_52high"]/span/text()
# -*- coding: utf-8 -*-

import scrapy

from scrapy import Spider
from scrapy.selector import Selector
import re

from moneycontrol.items import MoneycontrolItem
import MySQLdb

def ret0IfExist(arr):
    if len(arr):
        return str(arr[0]);


class FindetailsSpider(scrapy.Spider):
    name = "findetails"
    allowed_domains = ["moneycontrol.com"]
    start_urls = []
    def start_requests(self):
        conn = MySQLdb.connect(
            user='stocks_user',
            passwd='stocks_pass',
            db='stocks',
            host='localhost',
            charset="utf8",
            use_unicode=True
        )
        cursor = conn.cursor()
        cursor.execute(
            "select concat('http://www.moneycontrol.com/india/stockpricequote/chemicals/aartiindustries/',mc_symbol) from symbol_mc_map;"
        )
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)
            yield self.make_requests_from_url(row[0])            
        conn.close()

    def parse(self, response):
        # print self.start_urls
        item =MoneycontrolItem();
        item['book_value'] = ret0IfExist(Selector(response).xpath('//*[@id="mktdet_2"]/div[1]/div[3]/div[2]/text()').extract())
        item['symbol'] = ret0IfExist(Selector(response).xpath('//*[@id="nChrtPrc"]/div[4]/div[1]/text()[2]').extract())
        item['symbol'] = re.sub('NSE:','',item['symbol']).strip();
        item['pe'] = ret0IfExist(Selector(response).xpath('//*[@id="mktdet_2"]/div[1]/div[2]/div[2]/text()').extract())
        item['pc'] = ret0IfExist(Selector(response).xpath('//*[@id="mktdet_2"]/div[2]/div[2]/div[2]/text()').extract())
        item['industry_pe'] = ret0IfExist(Selector(response).xpath('//*[@id="mktdet_2"]/div[1]/div[6]/div[2]/text()').extract())
        item['nse_price'] = ret0IfExist(Selector(response).xpath('//*[@id="Nse_Prc_tick"]/strong/text()').extract())
        item['bse_price'] = ret0IfExist(Selector(response).xpath('//*[@id="Bse_Prc_tick"]/strong/text()').extract())
        item['sector'] = ret0IfExist(Selector(response).xpath('//*[@id="nChrtPrc"]/div[4]/div[1]/a/text()').extract())
        item['week_52_low'] = ret0IfExist(Selector(response).xpath('//*[@id="n_52low"]/text()').extract())
        item['week_52_high'] = ret0IfExist(Selector(response).xpath('//*[@id="n_52high"]/text()').extract())
        yield item
