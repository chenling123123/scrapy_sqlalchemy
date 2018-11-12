from scrapy import cmdline
import sys,time,os
from govcrawler.MethodWarehouse import MethodWarehouse



ISOTIMEFORMAT = '%Y-%m-%d %X'
picktime = str(time.strftime(ISOTIMEFORMAT, time.localtime()))
picktime = picktime.replace('-', '')
year = picktime[0:4]
month = picktime[4:6]
date = picktime[6:8]
yearmonth = year + month
# logger.setLevel(logging.DEBUG)
meth=MethodWarehouse()
path=meth.read_config("crawlerLogPath","1")

dir_name=os.path.join(path,year)
dir_name=os.path.join(dir_name,month)
dir_name=os.path.join(dir_name,date)

if not os.path.exists(dir_name):
    os.makedirs(dir_name)
#command="scrapy crawl policySpider -s LOG_FILE="+dir_name
#command="scrapy crawl govSpider -s LOG_FILE="+dir_name+"/all_log -a current_task_id="+sys.argv[1]
command="scrapy crawl govSpider -s LOG_FILE="+dir_name+"/all_log -a current_task_id=ff80808165b148aa0165b4bc313300c4"
cmdline.execute(command.split())
