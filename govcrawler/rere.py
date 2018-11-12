import re
import uuid
import os
a='5061389/images/2e72036ef4a3417b8dd0d52b108582e9.png'
dir_name='/usr/local/front_file_collection/image/2018/09/18'
serverimgpath1='http://103.235.234.108:15364/collection/image/2018/09/18'
imguid = uuid.uuid1()
imguid = str(imguid).replace('-', '')
if len(re.findall("png",a))>0:
    filename = os.path.join(dir_name, imguid + '.png')
    serverimgpath = os.path.join(serverimgpath1, imguid + '.png')
print(filename)
print(serverimgpath)