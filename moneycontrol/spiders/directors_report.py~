#get all the text of directors speech /html/body/center[2]/div/div/div[6]/div[3]/div[2]/div[1]/div/div[2]/table[2]/tbody/tr[3]/td/pre/text()
#get the years present /html/body/center[2]/div/div[1]/div[8]/div[3]/div[2]/div[2]/div[2]/div[1]/table[2]/tbody/tr[3]/td/text()
#symbol mc_symbol year key_type(ratios) key value created_at updated_at 
#tbody not required in xpath in scrapy
#frequent bugs 1)xpath getting changed- one div keeps toggling  on 6 or 8 
#/html/body/center[2]/div/div[1]/div[6]/div[3]/div[2]/div[2]/div[2]/div[1]/table[2]/tr[3]/td/text()
#/html/body/center[2]/div/div[1]/div[8]/div[3]/div[2]/div[2]/div[2]/div[1]/table[2]/tr[3]/td/text()

import scrapy
import sys
from scrapy import Spider
from scrapy.selector import Selector
import re
from scrapy.utils.response import open_in_browser
from moneycontrol.txt_data import MoneycontrolItem
import MySQLdb
from scrapy.http import Request
from scrapy.http import FormRequest

TOGGLING_DIV_NUM=6
TEXT_XPATH6='/html/body/center[2]/div/div/div[6]/div[3]/div[2]/div[1]/div/div[2]/table[2]/tr[3]/td/pre/text()';
TEXT_XPATH8='/html/body/center[2]/div/div/div[8]/div[3]/div[2]/div[1]/div/div[2]/table[2]/tr[3]/td/pre/text()';

YEARS_XPATH = '//*[@id="year_str"]/@value'
CURYEAR_XPATH = '//*[@id="sel_year"]/@value'

def ret0IfExist(arr):
    if len(arr):
        return str(arr[0].encode('UTF-8'));

class DataSpider(scrapy.Spider):
    name = "txt_data"           # name with which scrapy recognises spider
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
            "select concat('http://www.moneycontrol.com/annual-report/infosys/chairmans-speech/',mc_symbol,'#',mc_symbol),mc_symbol,symbol from symbol_mc_map ;"
        )
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)
            #yield self.ma ke_requests_from_url(row[0])            
            yield Request(url=row[0],meta={'symbol':row[2],'mc_symbol':row[1],'url':row[0],'posted':False},callback=self.parse)
            # yield FormRequest(url=row[0],meta={'symbol':row[2],'mc_symbol':row[1],'url':row[0]},method='POST',formdata={"end_year":"2017","nav":"next"},callback=self.parse)
        conn.close()

    def parse(self, response):
        # print self.start_urls
        #open_in_browser(response)
        allyears = ret0IfExist(Selector(response).xpath(YEARS_XPATH).extract())
        curyear = Selector(response).xpath(CURYEAR_XPATH).extract()
        if(curyear[0] and len(curyear[0])):
            curyear=curyear[0];
            curyear=curyear[:4];
            if(len(curyear)==0):
                return ;
        data = Selector(response).xpath(TEXT_XPATH8).extract()
        #print(data)
        if( len(data)==0):
            data = Selector(response).xpath(TEXT_XPATH6).extract()
            if(len(data)==0):                
                return ;
        data=ret0IfExist(data);
        # print(allyears);
        # print(curyear);
        #print(data);
        conn = MySQLdb.connect(
            user='stocks_user',
            passwd='stocks_pass',
            db='stocks',
            host='localhost',
            charset="utf8",
            use_unicode=True
        )
        cursor = conn.cursor();
        finData= MoneycontrolItem();
        finData['symbol']=str(response.meta['symbol']);
        finData['type']='ds'        # directors speech
        finData['year']=str(curyear);
        finData['data']=data;
        print('inserting');
        print(finData['symbol']);
        print(finData['type']);
        print(finData['year']);
        print('trying now');
        try:
            cursor.execute(
                "insert into stock_txt_data (symbol,data,type,year) values (%s,%s,%s,%s)"
                ,(finData['symbol'],finData['data'],finData['type'],finData['year'])
            )
        except:
            print("Unexpected error:", sys.exc_info())
            cursor.close()
        #print(finData);
        conn.commit();
        if(allyears is None):
            return;
        allyears = allyears.split(",");
        #all the other years have already been yielded in GET request
        #so post request should not yield more requests
        if(response.meta['posted']):
            return;
        for y in allyears:
            if(len(y)==0):
                continue;
            try:
                tempy=int(y[:4])
                y=int(y);
                curyear=int(curyear);
                if(tempy<=curyear):
                    continue;
            except:
                continue;
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/50.0.2661.102 Chrome/50.0.2661.102 Safari/537.36',
                'Content-Type':'application/x-www-form-urlencoded',
                'Referer':'http://www.moneycontrol.com/annual-report/infosys/chairmans-speech/IT',
            }
            formdata = {'sel_year':str(y),'sc_did':str(response.meta['mc_symbol'])};
            print(formdata)
            response.meta['posted']=True; # use this flag to post again or not
            yield FormRequest(response.url,method='POST',meta=response.meta,headers=headers,formdata = formdata,callback=self.parse)
        
