# -*- coding: UTF-8 -*-
# to dump a table to file
import datetime
import json
import sys
import urllib2
import MySQLdb as mysql
from sys import argv
import subprocess
from pymongo import MongoClient as mongodb
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
config=config.get("mongodb")
dbaddr=config.get("Addr")
username=config.get("User")
userpass=config.get("Pass")
client=mongodb(dbaddr, 27017)
db=client.admin
db.authenticate(username,userpass)
db=client.test
col=db.test
try:
  fh=open('../v6view.csv',mode='r')
  i=1 
  head=fh.readline()
  head=head.strip().split(',')
  while 1 :
    line=fh.readline()
    line=line.decode().strip().split(',')
    if line=="" :
      break
    doc=zip(head,line)
    doc=dict(doc)
    col.insert(doc)   
    i+=1
except Exception as e :
    pinrt "line: %s " % i
    print e
finally:
    fh.close()

