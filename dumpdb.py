# -*- coding: UTF-8 -*-
# to dump a table to file
import datetime
import json
import sys
import urllib2
import MySQLdb as mysql
from sys import argv
import subprocess
reload(sys)
sys.setdefaultencoding("utf8")
try :
   e=''
   fh=open('dbconfig.json',mode='r');#file handler
   config=fh.read()
except Exception as e:
   print e
finally:
   fh.close()
if e!='' :
   exit()
#resolve json file to abstract parameter
config=json.loads(config)
dbaddr=config.get("dbAddr")
username=config.get("rootName")
userpass=config.get("rootPass")
tabl = mysql.connect(dbaddr,username ,userpass , 'v6view', charset='utf8')
cur_tab = tabl.cursor();
cur_tab.execute("set names 'utf8'");  # be sure to encode in utf8
try :
   e=''
   child =subprocess.Popen("rm -f /var/lib/mysql-files/dbdumping.csv",shell=True)
   #remove previous dump file
   child.wait()
   cur_tab.execute("select * from (select 'id', 'ori','ori_ipv6','des','des_ipv6','date' ,'code','ipv4delay',\
   'ipv4doudong','ipv4lost','ipv6delay','ipv6doudong','ipv6lost' union select id,ori,ori_ipv6,des,des_ipv6,\
   date, code,ip4delay, ipv4doudong, ipv4lost,ipv6delay,ipv6doudong,ipv6lost from \
   nodes_ping_each) tab into outfile '/var/lib/mysql-files/dbdumping.csv' \
   fields terminated by ',' ")

except Exception as e :
   print e
finally :
   cur_tab.close()
   tabl.close()
if e=='' :
   #child=subprocess.Popen("cd /var/lib/mysql-files",shell=True)
   #child.wait()
   subprocess.Popen("zip  -j /opt/lampp/htdocs/pma/dbd.zip /var/lib/mysql-files/dbdumping.csv",shell=True)
   # -j to remove path information
