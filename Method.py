# -*- coding: UTF-8 -*-
import time
import os
import re
import requests
from scrapy.selector import Selector
import datetime

def extractdate(date,*args):
    """
    时间过滤，并转换正确的时间格式(取字符串的最后一项日期值)
    """
    crawldate = datetime.datetime.now()
    if date and crawldate:
        date = date.replace(".", "-").replace("/", "-").replace("\n","").replace("\\", "-")
        re_en = re.compile("(201[1-9]-\d{1,2}-\d{1,2}[\s]+\d{1,2}:\d{1,2}:\d{1,2})")
        re_cn = re.compile(u"(201[1-9]年\d{1,2}月\d{1,2}日[\s]+\d{1,2}时\d{1,2}分\d{1,2})秒")
        re_d_en = re.compile("(201[1-9]-([1-9]|0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]|[1-9]))")
        re_d_cn = re.compile(u"(201[1-9]年\d{1,2}月\d{1,2})日")
        re_m = re.compile("(([1-9]|0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]|[1-9]))")
        re_d = re.compile(u"(昨天|前天|今天)")
        re_d_dn = re.compile(u"(\d{1,2})天前")
        re_d_mn = re.compile(u"(\d{1,2})月前")
        re_d_xn = re.compile(u"(\d{1,2})小时前")
        re_d_mmn = re.compile(u"(\d{1,2})分钟前")

        if re_en.search(str(date)):
            date = re_en.search(str(date)).group(1)
        elif re_cn.search(str(date)):
            date = re_cn.search(str(date)).group(1)
            date = date.replace("年", "-").replace("月", "-").replace("日", "").replace("时", ":").replace("分",":").replace("秒", "")
        elif re_d_en.search(str(date)):
            date = re_d_en.search(str(date)).group(1)
            date = date + " 00:00:00"
        elif re_d_cn.search(str(date)):
            date = re_d_cn.search(str(date)).group(1)
            date = date.replace("年", "-").replace("月", "-").replace("日", "") + " 00:00:00"
        elif re_m.search(str(date)):
            date = re_m.search(str(date)).group(1)
            date = "2017-" + date + " 00:00:00"
        elif re_d.search(str(date)):
            if date == "今天":
                date = crawldate.strftime('%Y-%m-%d %H:%M:%S')
            elif date == "昨天":
                date = crawldate - datetime.timedelta(days=1)
                date = date.strftime('%Y-%m-%d %H:%M:%S')
            elif date == "前天":
                date = crawldate - datetime.timedelta(days=2)
                date = date.strftime('%Y-%m-%d %H:%M:%S')
        elif re_d_dn.search(str(date)):
            date = re_d_dn.search(str(date)).group(1)
            date = crawldate - datetime.timedelta(days=int(date))
            date = date.strftime('%Y-%m-%d %H:%M:%S')
        elif re_d_mn.search(str(date)):
            date = re_d_mn.search(str(date)).group(1)
            date = crawldate - datetime.timedelta(days=int(date) * 30)
            date = date.strftime('%Y-%m-%d %H:%M:%S')
        elif re_d_xn.search(str(date)):
            date = re_d_xn.search(str(date)).group(1)
            date = crawldate - datetime.timedelta(hours=int(date))
            date = date.strftime('%Y-%m-%d %H:%M:%S')
        elif re_d_mmn.search(str(date)):
            date = re_d_mmn.search(str(date)).group(1)
            date = crawldate - datetime.timedelta(minutes=int(date))
            date = date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date=""
        return date

def time_filter(date,*args):
    """
    时间过滤，并转换正确的时间格式(取字符串的最后一项日期值)
    """
    crawldate = datetime.datetime.now()
    if date and crawldate:
        date = date.replace(".", "-").replace("/", "-").replace("\n", "").replace("\\", "-")
        re_en = re.compile("(201[1-9]-\d{1,2}-\d{1,2}[\s])+\d{1,2}:\d{1,2}:\d{1,2}")
        re_cn = re.compile(u"(201[1-9]年\d{1,2}月\d{1,2}日[\s])+\d{1,2}时\d{1,2}分\d{1,2}秒")
        re_d_en = re.compile("(201[1-9]-(0[1-9]|1[0-2]|[1-9])-(0[1-9]|[12][0-9]|3[01]|[1-9]))")
        re_d_cn = re.compile(u"(201[1-9]年\d{1,2}月\d{1,2})日")
        re_n_cn = re.compile(u"(\d{2}年\d{1,2}月\d{1,2})日")
        re_m = re.compile("(([1-9]|0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]|[1-9]))")
        re_d = re.compile(u"(昨天|前天|今天)")
        re_d_dn = re.compile(u"(\d{1,2})天前")
        re_d_mn = re.compile(u"(\d{1,2})月前")
        re_d_xn = re.compile(u"(\d{1,2})小时前")
        re_d_mmn = re.compile(u"(\d{1,2})分钟前")
        re_1=re.compile("(201[1-9][0,1][0-9][0-3][0-9])")

        if re_en.search(str(date)):
            date = re_en.search(str(date)).group(1)
        elif re_cn.search(str(date)):
            date = re_cn.search(str(date)).group(1)
            date = date.replace("年", "-").replace("月", "-").replace("日", "")
        elif re_n_cn.search(str(date)):
            date = re_n_cn.search(str(date)).group(1)
            date = "20"+date.replace("年", "-").replace("月", "-").replace("日", "")
        elif re_d_en.search(str(date)):
            date = re_d_en.search(str(date)).group(1)
            date = date
        elif re_d_cn.search(str(date)):
            date = re_d_cn.search(str(date)).group(1)
            date = date.replace("年", "-").replace("月", "-").replace("日", "")
        elif re_m.search(str(date)):
            date = re_m.search(str(date)).group(1)
            date = "2018-" + date
        elif re_d.search(str(date)):
            if date == "今天":
                date = crawldate.strftime('%Y-%m-%d')
            elif date == "昨天":
                date = crawldate - datetime.timedelta(days=1)
                date = date.strftime('%Y-%m-%d')
            elif date == "前天":
                date = crawldate - datetime.timedelta(days=2)
                date = date.strftime('%Y-%m-%d')
        elif re_d_dn.search(str(date)):
            date = re_d_dn.search(str(date)).group(1)
            date = crawldate - datetime.timedelta(days=int(date))
            date = date.strftime('%Y-%m-%d')
        elif re_d_mn.search(str(date)):
            date = re_d_mn.search(str(date)).group(1)
            date = crawldate - datetime.timedelta(days=int(date) * 30)
            date = date.strftime('%Y-%m-%d')
        elif re_d_xn.search(str(date)):
            date = re_d_xn.search(str(date)).group(1)
            date = crawldate - datetime.timedelta(hours=int(date))
            date = date.strftime('%Y-%m-%d')
        elif re_d_mmn.search(str(date)):
            date = re_d_mmn.search(str(date)).group(1)
            date = crawldate - datetime.timedelta(minutes=int(date))
            date = date.strftime('%Y-%m-%d')
        elif re_1.search(str(date)):
            temp = re_1.search(str(date)).group(1)
            date=temp[0:4]+"-"+temp[4:6].zfill(2)+"-"+temp[6:8].zfill(2)
        else:
            date = ""
        return datecheck(date)

def datecheck(date):
    if re.search("201[1-9]-\d{1,2}-\d{1,2}",date):
        return date
    else:
        return ""


def intercept(source,li):
    """前后截取"""
    source="".join(source)
    str1 = re.split(li[0],source, 1)
    if len(str1) != 1:
        str2 = re.split(li[1], str1[1], 1)[0]
    else:
        print('截取未取到数据')
        str2 = ""
    return str2

def extractre(source,pattern,loop=0):
    """正则提取，loop是否循环提取"""
    source="".join(source)
    strs = re.search(pattern, source)
    if strs:
        if loop:
            newstr=re.findall(pattern,source)
        else:
            newstr=strs.group(1)
    else:
        newstr=""
    return newstr

def localtime(*args):
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))

def new_connect(source,li):
    """加前后缀"""
    source="".join(source)
    newstr=str(li[0])+source+str(li[1])
    print(newstr)
    return newstr

def re_extract(source,li,text):
    """为空再次提取
    :param li:[0]xpath,[1]截取前字符，[2]截取后字符
    """
    if not source:
        source=intercept(text,li)
    return source

def add_new(source,list):
    new="".join(source)
    new=new.join(list)
    return new

def delete_biaoqian(text):
    """:param li:保留的标签列表
    """
    lists=['a','img','p','table','tr','td','font','br','div','style','script','b','strong','iframe',
           'object','li','ul','dd','dt','sub','sup','h1','h2','h3','h4','h5','h6','h7',
           'frame','form','span','hr','em','!--','html','head','meta','title','input','center',
           'section','tbody','voice']

    for i in lists:
        str1='<'+i+'.*?'+'>'
        str2='</'+i+'>'
        reg=re.compile(str1)
        reg1=re.compile(str2)
        text=reg.sub('',text)
        text=reg1.sub('',text)
    return text

def str_replace(source,li):
    source="".join(source)
    if source:
        reg = re.compile(li[0])
        text = reg.sub(li[1], source)
    else:
        text=""
    return text

def delete_blank(source,*args):
    text="".join(source)
    strlist=['\\n','\\r','\\t','&nbsp;',"\xa0","\u3000","\n",'\r','\t']
    for str in strlist:
        text = text.replace(str, '')
    return text


def decode(source,*args):
    """字符串解码"""
    match = re.search(r"\\u.*", source)
    if match:
        source = source.encode().decode('unicode_escape')
    return source

def escape(source,*args):
    if source:
        source="".join(source)
        source=source.replace("&quot;",'"').replace("&amp;", '&').\
            replace("&lt;", '<').replace("&gt;", '>').replace("&nbsp;", ' ')
    return source

def xpath(source,li):
    """用xpath方法提取数据"""
    try:
        str=source.xpath(li[0]).extract()
        if li[-1]=="1":
            text="".join(str)
        else:
            text=str[0]
    except:
        print('未取到数据')
        text = ""
    return text

def re_xpath(source,li,text):
    """为空再次提取
    :param li:[0]xpath,[1]截取前字符，[2]截取后字符
    """
    if not source:
        try:
            source=text.xpath(li[0]).extract()[0]
        except:
            source=""
            print("xpath再次提取失败")
    return source

def name_filter(result,*args):
    list_chuan = ["双创","创新创业","创响中国","放管服","营商"]
    i=0
    try:
        if "2018-" in str(result["publishtime"]):
            for l in list_chuan:
                if l in result["content"]:
                    i=1
    except:
        pass
    return i

def url_filter(result,*args):
    i=0
    try:
        if "gov.cn" in result["url"]:
            i=1
    except:
        pass
    return i



if __name__ == '__main__':
    a='{"code":1,"message":"","data":{"id":163412,"article":{"id":39790,"publicAccount":{"id":473,"name":"黄河敏捷开发","weixin":"gh_9c3a3a80244d","intro":"","body":"","image":"http://ss.csdn.net/p?http://wx.qlogo.cn/mmhead/Q3auHgzwzM5ibapmJJGPBAuMJ8AtS9LYalDmGtaOXkRI82Zlp1sPVIA/0","href":null,"biz":"MzI0Njg4NDcwMw==","category":{"id":10,"keyName":"sd","displayName":"软件研发","createdAt":1487578543000,"updatedAt":1487578543000,"status":1},"createdAt":1496812532000,"updatedAt":1496812532000,"status":1,"recommend":0,"qrcode":"http://mp.weixin.qq.com/mp/qrcode?scene=10000001&size=120&__biz=MzI0Njg4NDcwMw==&mid=2247483671&idx=1&sn=c95205a02fef2f08386458d4b66e6c92","articleCount":0,"viewCount":0},"category":{"id":10,"keyName":"sd","displayName":"软件研发","createdAt":1487578543000,"updatedAt":1487578543000,"status":1},"biz":"MzI0Njg4NDcwMw==","mid":"2247483737","idx":1,"sn":"1dca2aee4187b12b1a7abc589a8f6e5d","author":"林冰玉","content":"","contentUrl":"http://mp.weixin.qq.com/s?__biz=MzI0Njg4NDcwMw==&mid=2247483737&idx=1&sn=1dca2aee4187b12b1a7abc589a8f6e5d&chksm=e9b93169deceb87f9d3bcdc9e54fbc20042076ad4d2369627f2cf39247a86ffea3a87defcedf&scene=27#wechat_redirect","cover":"http:\\/\\/mmbiz.qpic.cn\\/mmbiz_png\\/ibJwvCS7zg8wu45XvIZUOcj4vSiaau7E9WgOxAW8wk9GVYpWibFzco4GBo31sx28J6BbiciaEfClzyAoFkicvUKUS3bw\\/0?wx_fmt=png","digest":"关于showcase的正确做法都是围绕“专业（Professional）”和“高效（Efficient）”展开的。","isMulti":0,"sourceUrl":"http:\\/\\/blog.csdn.net\\/huver2007\\/article\\/details\\/71514090","title":"敏捷实践Showcase的七宗罪｜TW洞见","description":null,"datetime":1499819888000,"status":1,"viewCount":326,"praiseCount":20,"commentCount":0,"createdAt":1499821248000,"updatedAt":1500442130000,"origin":"proxy","recommend":0},"url":"http://mp.weixin.qq.com/s?__biz=MzI0Njg4NDcwMw==&mid=2247483737&idx=1&sn=1dca2aee4187b12b1a7abc589a8f6e5d&chksm=e9b93169deceb87f9d3bcdc9e54fbc20042076ad4d2369627f2cf39247a86ffea3a87defcedf&scene=27#wechat_redirect","title":"敏捷实践Showcase的七宗罪｜TW洞见","source":"", '
