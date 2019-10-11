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
col=db.chinacache
head=[ "ipaddr",  "addr", "addr_2", "addr_3", "agency","date", "max", "average", "purpose", "status","YM","day"]
try:
  fh=open('./dltemp1',mode='r')
  i=1 
  while 1 :
    line=fh.readline()
    if line=='' :
        break
    line=line.decode().strip().split(',')
    #decode() for utf8
    #strip() to remove blank key or "\r" "\n"
    #split() to break a string into a list
    line=line[:-1] ; # remove last filename field
    doc=zip(head,line) ; # make key value tuple pair
    doc=dict(doc)      ; # make key value document    
    doc["average"]=float(doc["average"])
    #converting string into float
    doc["max"]=float(doc["max"])
#convert column type :
#db.chinacache.find().forEach(function(doc){doc.average=parseFloat(doc.average); doc.max=parseFloat(doc.max);db.order.save(doc)})    
    col.insert(doc)   ;print i; # insert into db
    i+=1
except Exception as e :
    print e
finally:
    fh.close()
    client.close()

