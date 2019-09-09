#detect if every node in database is active
#with threading 
import threading
import time
import sys
import MySQLdb as mysql
import socket
import select
import os
import urllib2
import json

def connect_remote(cmmd):
    req = urllib2.Request(cmmd)
    try:
        reslt = urllib2.urlopen(req, data=None, timeout=15)
        return reslt.read()
    except Exception as e:
        return e
    


version='4'
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
#fp=open("log",'wb')

cur_tab.execute("set names 'utf8'");  # be sure to encode in utf8
# tabl=sqlite3.connect('v6view.s3db',check_same_thread = False)
# tabl.text_factory = lambda x: unicode(x, "utf-8", "ignore")
# cur_tab=tabl.cursor()
#cur_tab.execute("select url, type from urllist");urls = cur_tab.fetchall()
cur_tab.execute("select id, name,  ipv4, ipv6 from v6view")
nodes= cur_tab.fetchall()
cur_tab.execute("truncate nodestatus")
# fetch all the url in the list


for  node in nodes :
        url = "www.qq.com";i=0
        if version == '4':
                para1 = node[2];  # source ipv4addr
        else:
                para1 = node[3];
                # source ipv6 addr
        para2 = url
        print node ; #fp.write(str(node))
        if version == '6':
                cmd = 'http://[' + para1 + ']:9050/'
        else:
                cmd = 'http://' + para1 + ':9050/';  # /site/domainARecord?website=+para2
        req = cmd + 'site/homePage?website=' + para2 + '&status=0&ipstatus=4'
        result=connect_remote(req)
        print "return result %s" %  result; #fp.write(str(result)+'\r')
        cur_tab.execute("insert nodestatus(id, result) value(%d,'%s' )" % (node[0], result)) 
        cur_tab.execute("commit")
cur_tab.execute("update v6view set httpstat='500' where httpstat='200'")
cur_tab.execute("commit")
cur_tab.execute("update v6view, nodestatus set v6view.httpstat='200' where \
v6view.id=nodestatus.id and nodestatus.result regexp '^[1-9][0-9]*$'")
cur_tab.execute("commit")
cur_tab.close()
tabl.close()

