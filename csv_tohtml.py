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

if len(argv) < 2:
    print  argv
    print "Usage:\n%s csvfilename\nwrite result to a file named dumping" %argv[0]
    exit(0)
else:
    csvfile=argv[1]

'''
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
config=config.get("mongodb")
dbaddr=config.get("Addr")
username=config.get("User")
userpass=config.get("Pass")
client=mongodb(dbaddr, 27017)
db=client.admin
db.authenticate(username,userpass)
db=client[dbname]

'''
try:
  fh=open(csvfile,mode='r')
  dpfh=open("dumping.htm",mode='w')
  i=1 
  head=fh.readline()
  head=head.decode().strip().split(',')
  dpfh.write('<!DOCTYPE html>\n<html lang="zh-cn">\n<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<title>代码集</title>\n<style>.p1{text-indent: 40px;}</style>\n</head>\n<body>\n')
  code=' ' 
  while 1 :
    line=fh.readline()
    if line=='' :
       if i >1 :
         dpfh.write("<p>]</p>\n")
       break
    line=line.decode().strip().split(',')
    doc=zip(head,line) ; # make key value tuple pair
    #doc=dict(doc)      ; #dict is not necessary
    # make key value document    
    #doc["index"]=i
    print doc
    setcode=doc[2][1] ; #read the setcode colum
    entry=doc[4:6]
    del doc[4:6]
    if setcode != code :
    # same set? if not  i
       code=setcode
       if i!=1 :
         dpfh.write("<p>]</p>\n")
       index="<h2><strong>"+str(i)+"</strong></h2>\n"
       i+=1
       dpfh.write(index)
       for kv in doc :
         dpfh.write('<p>')
         dpfh.write(str(kv[0]).encode('utf-8')); #key part 中文写入
         if kv[1]=='' or kv[1] is None :
            value=' '
         else :
           value=kv[1]
         dpfh.write(': ')
         dpfh.write(str(value).encode('utf-8')); #value 
         dpfh.write('</p>\n')
       dpfh.write('<p>代码集内容: [ </p>\n')
    dpfh.write('<p class="p1">')
    dpfh.write(dict(entry)[u'代码'].encode('utf-8')) 
    dpfh.write('：')
    dpfh.write(dict(entry)[u'名称'].encode('utf-8')) 
    dpfh.write('</p>\n')    
except Exception as e :
    #pinrt "lindde: %s ", % i
    print e
finally:
    dpfh.write("</body></html>")
    fh.close()
    dpfh.close()

