# -*- coding: UTF-8 -*-
# import sqlite3
import datetime
# import os
import json
import sys
import urllib2
import MySQLdb as mysql
from sys import argv
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
config=json.loads(config)
dbaddr=config.get("dbAddr")
username=config.get("rootName")
userpass=config.get("rootPass")
tabl = mysql.connect(dbaddr,username ,userpass , 'v6view', charset='utf8')
cur_tab = tabl.cursor();
cur_tab.execute("set names 'utf8'");  # be sure to encode in utf8
# tabl=sqlite3.connect('v6view.s3db',check_same_thread = False)
# tabl.text_factory = lambda x: unicode(x, "utf-8", "ignore")
# cur_tab=tabl.cursor()
try :
   cur_tab.execute("select * from nodes_ping_each into outfile '/var/lib/mysql-files/dbdumping.csv'\
   fields terminated by ',' ")
except Exception as e :
   print e
finally :
  cur_tab.close()
  tabl.close()

