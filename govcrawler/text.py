import pymysql
import chardet
from urllib import request
import requests
import urllib

# a=requests.get('http://www.xuchang.gov.cn/EpointWebBuilder/zNJSAction.action?cmd=getOpenDetail&infoid=cab9a1a8-2e97-4e4b-9d81-170ad060b243')
#
# #b=chardet.detect(a.text)
#
# #print(a.text)
# #print(b['encoding'])
# byte1 = bytes(a.text,"ascii")
# print(byte1)
# #print(byte1.decode("gb2312"))
# c='\":[{\"identifier\":\"11411000005747138B\/201810-02277\",\"cate\":\"\u8BB8\u660C\u5E02\u4EBA\u6C11\u653F\u5E9C,

#f = urllib.request.urlopen('http://www.yanan.gov.cn/info/iList.jsp?site_id=GKya&cat_id=11779&node_id=GKya&cur_page=1')
# byte1 = bytes(f.text,"ascii")
# print(type(f[10]))
# print(byte1.decode("gb2312"))
# print(f[10].decode('utf-8'))
f=requests.get('http://www.yanan.gov.cn/info/iList.jsp?site_id=GKya&cat_id=11779&node_id=GKya&cur_page=1')
print(f.text)