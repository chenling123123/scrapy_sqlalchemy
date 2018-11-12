# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from govcrawler.model import Gov_Table_Url, Gov_Table, engine,Policy_statistics
from sqlalchemy.orm import sessionmaker
from govcrawler.items import GovcrawlerItemMiddle,GovcrawlerItemLast
import sys
from govcrawler.mongodb_job import  CMongo
from govcrawler.MethodWarehouse import MethodWarehouse
import datetime
from govcrawler.spiders import spider_demo

class GovcrawlerPipeline(object):
    def __init__(self):
        self.item_size=0
        self.item_count=0
        self.cmongo = CMongo()
        self.MethodWarehouse=MethodWarehouse()
        self.spider_id=""

    def process_item(self, item, spider):
        if isinstance(item, GovcrawlerItemMiddle):
            #mongoDB中间表存储
            # self.cmongo.add_one("policy_data_mid",{
            #     "title": item['title'],"url":item['url'],"state":item['state']
            # })
            self.spider_id = spider.current_task_id
            #mysql存储

            self.session.add(Gov_Table_Url(**item))

            return item
        elif isinstance(item, GovcrawlerItemLast):
            self.item_count = self.item_count + 1
            self.item_size = self.item_size+sys.getsizeof(item['content']) + sys.getsizeof(item['pub_time'])+sys.getsizeof(item['title'])+sys.getsizeof(item['url'])
           
            item=self.MethodWarehouse.imgDownload(item)
            #mongoDB数据持久化
            # self.cmongo.add_one("policy_data_last",{
            # "title":item['title'],"url":item['url'], "content":item['content'], "pubTime":item['pubTime'], "pickTime":item['pickTime'],
            #                        "img_path":item['img_path'], "attachment_path":item['attachment_path'], "state":item['state']})
            # self.cmongo.update("policy_data_mid",item['url'])
            #mysql数据持久化
            print(item['url'])
            query = self.session.query(Gov_Table_Url).filter_by(url=item['url']).update({Gov_Table_Url.state: 1})
            policy_statistics = self.session.query(Policy_statistics).filter_by(id=self.spider_id).update(
                {Policy_statistics.data_total: self.item_size, Policy_statistics.data_count: self.item_count,
                 Policy_statistics.stop_time: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            self.session.add(Gov_Table(**item))
            self.session.commit()
            return item

    def open_spider(self, spider):

        Session = sessionmaker(bind=engine)
        self.session = Session()


    def close_spider(self, spider):
        # 日志数据持久化
        policy_statistics =self.session.query(Policy_statistics).filter_by(id=self.spider_id).update(
            {Policy_statistics.data_total:self.item_size,Policy_statistics.data_count:self.item_count,Policy_statistics.stop_time:datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
             Policy_statistics.task_state:1})

        self.session.commit()
        self.session.close()

