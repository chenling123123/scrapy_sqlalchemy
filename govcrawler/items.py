# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class GovcrawlerItemMiddle(Field):

    id=Field()
    title=Field()
    url = Field()
    state=Field()
class GovcrawlerItemLast(Field):
    id = Field()
    current_task_id=Field()
    title = Field()
    url = Field()
    content = Field()
    pub_time = Field()
    pick_time = Field()
    img_path = Field()
    attachment_path=Field()
    front_name=Field()
    front_id=Field()
    state=Field()