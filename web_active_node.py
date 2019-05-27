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
dbaddr = "127.0.0.1"
tabl = mysql.connect(dbaddr, 'root', 'rtnet', 'v6view', charset='utf8')
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
# 如果表里所有Regstat为1，说明已经跑完，重新把?regstat设为0，重新进行测试

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
fp.close()		
cur_tab.close()
tabl.close()

