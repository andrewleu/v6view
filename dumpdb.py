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
#read configuration from a json file
cur_tab = tabl.cursor();
cur_tab.execute("set names 'utf8'");  # be sure to encode in utf8
cur_tab.execute("select date_sub(curdate(),INTERVAL WEEKDAY(curdate()) + 0 DAY)")
file_daystr=cur_tab.fetchone()[0];
#the date of monday ofr this week
start_time=file_daystr.isoformat()+' '+'00:00:00'
try :
   e=''
   child =subprocess.Popen("rm -f /var/lib/mysql-files/dbdumping.csv",shell=True)
   #remove previous dump file
   child.wait()
   cur_tab.execute("select min(id) from test6 where date> '%s'" % start_time)
   minid=cur_tab.fetchone()
   #the lowest id of the entry of this week
   cur_tab.execute("select * from (select 'id', 'ori','ori_ipv4','ori_ipv6','des','des_ipv4','des_ipv6','date' ,'code','ipv4delay',\
   'ipv4doudong','ipv4lost','ipv6delay','ipv6doudong','ipv6lost' union select id,ori,ori_ipv4,ori_ipv6,des,des_ipv4,des_ipv6,\
   date, code,ip4delay, ipv4doudong, ipv4lost,ipv6delay,ipv6doudong,ipv6lost from \
   nodes_ping_each where id>%d) tab into outfile '/var/lib/mysql-files/dbdumping.csv' \
   fields terminated by ',' " % minid); #dumping
except Exception as e :
   print e
finally :
   cur_tab.close()
   tabl.close()
if e=='' :
   print datetime.datetime.now().isoformat()
   command_str="zip  -j /opt/lampp/htdocs/pma/dbd"+file_daystr.isoformat().replace("-",'')+".zip"\
   +' '+'/var/lib/mysql-files/dbdumping.csv'
   subprocess.Popen(command_str,shell=True).wait()
   # -j to remove path information

