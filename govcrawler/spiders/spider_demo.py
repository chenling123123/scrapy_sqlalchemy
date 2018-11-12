import scrapy
from scrapy.selector import Selector
from bs4 import BeautifulSoup
from govcrawler.items import GovcrawlerItemMiddle,GovcrawlerItemLast
from scrapy.http import Request
import time
from govcrawler.mongodb_job import CMongo
from govcrawler.model import Gov_Table_Url
from govcrawler.MethodWarehouse import MethodWarehouse

class GovSpider(scrapy.Spider):
    name="govSpider"
    start_urls=[]
    #first_url='http://www.chinasei.com.cn/swcy/swyy/index.html'
    start_url='http://sousuo.gov.cn/column/30144/'
    last_url='.htm'
    ISOTIMEFORMAT = '%Y-%m-%d %X'

    def __init__(self,current_task_id):
        #调度平台传递的参数
        self.current_task_id = current_task_id
        #self.task_id = task_id
        self.mongo=CMongo()
        self.gov_Table_Url=Gov_Table_Url()
        self.method=MethodWarehouse()
        self.front_name=self.method.read_config("CHILDNODE","0")
        self.front_id=self.method.read_config("CHILDNODE","1")
    def start_requests(self):


        for i in range(6):
            self.start_urls.append(self.start_url+str(i)+self.last_url)
        for url in self.start_urls:
            print(url)
            yield Request(url=url, callback=self.parse)


    def parse(self, response):
        selector = Selector(response)

        text0 = selector.xpath('/html/body/div[2]/div/div[2]/div[2]/ul').extract_first()
        if text0:
            soup = BeautifulSoup(text0, "lxml")
            if soup.find_all('li'):
                a_s = soup.find_all('li')
                item=GovcrawlerItemMiddle()
                for li in a_s:
                    if li.find('span'):
                        span=li.find('span')
                        publishTime=span.text
                    if li.find('a'):
                        a = li.find('a')
                        title=a.text
                        mid_url=a.get('href')
                        if mid_url[0:2]=='./':
                            item['state']=2
                        else:
                            item['state']=0
                        item['url']=mid_url
                        item['title']=title
                        #mongoDB中间表数据去重
                        # if self.mongo.get_one("policy_data_mid",item['url']):
                        #     print("该数据已经采集")
                        if self.gov_Table_Url.sele_by_url(item['url']):

                            print("该数据已经采集"+item['url'])
                        else:
                            yield item
                            yield Request(url=mid_url, meta={"url":mid_url,"title":title,"publishTime":publishTime},callback=self.parse_last)


    def parse_last(self,response):
        selector = Selector(response)
        item=GovcrawlerItemLast()
        item['url'] = response.meta["url"]
        item['title'] = response.meta["title"]
        item['content'] = selector.xpath('//*[@id="UCAP-CONTENT"]').extract_first()
        item['pub_time']=response.meta["publishTime"].replace(".","-")
        item['pick_time']=str(time.strftime(self.ISOTIMEFORMAT, time.localtime()))
        if len(item['pub_time']) ==11:
            item['pub_time'] = item['pub_time']+"00:00:00"
        elif len(item['pub_time']) ==16:
            item['pub_time'] = item['pub_time'] + ":00"
        else:
            item['pub_time']=item['pub_time']
        item['img_path']=''
        item['attachment_path']=''
        item['current_task_id']=self.current_task_id
        method=MethodWarehouse()
        item['id']=str(method.uuid()).replace('-','')
        item['front_name']=self.front_name
        item['front_id']=self.front_id
        yield item
