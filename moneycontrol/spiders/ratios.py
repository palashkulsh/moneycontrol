#get all the rows of financial ratios /html/body/center[2]/div/div[1]/div[8]/div[3]/div[2]/div[2]/div[2]/div[1]/table[2]/tbody/tr
#get the years present /html/body/center[2]/div/div[1]/div[8]/div[3]/div[2]/div[2]/div[2]/div[1]/table[2]/tbody/tr[3]/td/text()
#symbol mc_symbol year key_type(ratios) key value created_at updated_at 
#tbody not required in xpath in scrapy
#frequent bugs 1)xpath getting changed


import scrapy
import sys
from scrapy import Spider
from scrapy.selector import Selector
import re
from scrapy.utils.response import open_in_browser
from moneycontrol.ratios import RatioItem
import MySQLdb
from scrapy.http import Request
from scrapy.http import FormRequest

def ret0IfExist(arr):
    if len(arr):
        return str(arr[0]);

class RatiosSpider(scrapy.Spider):
    name = "ratios"
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
            "select concat('http://www.moneycontrol.com/financials/aartiindustries/ratiosVI/',mc_symbol,'#',mc_symbol),mc_symbol,symbol from symbol_mc_map where symbol in ('ATNINTER','BIRLACABLE','CUPID','ENDURANCE','FCONSUMER','GNA','HPL','ICICIPRULI','IDFNIFTYET','KREBSBIO','LTTS','MARATHON','MASKINVEST','MAZDA','REL100NAV','RELBANKNAV','RELCONSNAV','RELDIVNAV','RELGOLDNAV','RELNV20NAV','RENIFTYNAV','SABEVENTS','SPECTACLE','TVVISION','BIRLAERIC',  'DUNCANSLTD',  'ELDERPHARM',  'ERAINFRA',  'IVZINGOLD',  'IVZINNIFTY',  'JCHAC',  'LALPATHLAB',  'LICNETFSEN',  'LICNFNHGP',  'MIDCAPIWIN',  'N100',  'NV20IWIN',  'PREMIER',  'RELNV20',  'SETF10GILT',  'SHK');"
        )
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)
            #yield self.make_requests_from_url(row[0])            
            yield Request(url=row[0],meta={'symbol':row[2],'mc_symbol':row[1],'url':row[0]},callback=self.parse)
            # yield FormRequest(url=row[0],meta={'symbol':row[2],'mc_symbol':row[1],'url':row[0]},method='POST',formdata={"end_year":"2017","nav":"next"},callback=self.parse)
        conn.close()

    def parse(self, response):
        # print self.start_urls
        #open_in_browser(response)
        years = Selector(response).xpath('/html/body/center[2]/div/div[1]/div[8]/div[3]/div[2]/div[2]/div[2]/div[1]/table[2]/tr[3]/td/text()').extract()
        lastYear=0;
        if(len(years)>0):
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print(years)
            try:
                lastYear = years[len(years)-1];
                lastYear = lastYear.split(" ")
                lastYear = int(lastYear[1]);
                lastYear = lastYear +2000;
            except:
                lastYear=0;
                print('not found years')
        dataRows = Selector(response).xpath('/html/body/center[2]/div/div[1]/div[8]/div[3]/div[2]/div[2]/div[2]/div[1]/table[2]/tr')
        print("after")
        conn = MySQLdb.connect(
            user='stocks_user',
            passwd='stocks_pass',
            db='stocks',
            host='localhost',
            charset="utf8",
            use_unicode=True
        )
        for dataRow in dataRows:
            print(dataRow)
            actualData = dataRow.xpath('td/text()').extract();
            if(len(actualData)>len(years)):
                for index in range(0,len(years)):
                    y = str(years[index]);
                    y = y.split(" ");
                    finData = RatioItem();
                    finData['symbol'] = str(response.meta['symbol']);
                    # finData['mc_symbol'] = str(response.meta['mc_symbol']);                
                    finData['key_text'] = str(actualData[0]);
                    finData['value'] = str(actualData[index+1]);
                    finData['year'] = int(y[1])+2000;
                    finData['month'] = str(y[0]);
                    finData['key_type'] = 'ratios';
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "insert into fin (symbol,key_text,key_type,value,year,month) values (%s,%s,%s,%s,%s,%s)"
                            ,(finData['symbol'],finData['key_text'],finData['key_type'],finData['value'],finData['year'],finData['month'])
                        )
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                    cursor.close()
                    print(finData);

            conn.commit()
        if(lastYear>0):
            print("(((((((((((((((((((((((((((((((((((((")
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
            }
            formdata = {"end_year":str(lastYear)+'03',"nav":"next"};
            print(formdata)
            yield FormRequest(response.url,method='POST',meta=response.meta,headers=headers,formdata = formdata,callback=self.parse)
        
