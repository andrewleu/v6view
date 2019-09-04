# -*- coding: UTF-8 -*-
# import sqlite3
import datetime
# import os
import json
import sys
import urllib2
import MySQLdb as mysql
from sys import argv

def connect_remote(cmmd):
    req = urllib2.Request(cmmd)
    e=""
    try:
        reslt = urllib2.urlopen(req, data=None, timeout=15)
    except Exception as e:
        print e
    if e :
        return '{"code":"0"}'
    else :
      return reslt.read()

if len(argv) < 2:
    version = '4'
    print "input with -4 or -6, by default use version 4"
else:
    if argv[1] == '-4':
        version = '4'
    elif argv[1] == '-6':
        version = '6'
    else:
        print "input with -4 or -6, by default use version 4"
        version = '6'
print version
reload(sys)
sys.setdefaultencoding("utf8")
dbaddr = "127.0.0.1"
tabl = mysql.connect(dbaddr, 'root', 'rtnet', 'v6view', charset='utf8')
cur_tab = tabl.cursor();
cur_tab.execute("set names 'utf8'");  # be sure to encode in utf8
# tabl=sqlite3.connect('v6view.s3db',check_same_thread = False)
# tabl.text_factory = lambda x: unicode(x, "utf-8", "ignore")
# cur_tab=tabl.cursor()
version='6'
if not cur_tab.execute("select id,name, prov, city, ipv4, ipv6 from 3main_node where regstat='0'") : 
#v6viewv is view of v6view for coding convinience; the previous one is 4main_node view
#    l=cur_tab.fetchall(); print l
    cur_tab.execute("update v6view set regstat='0' ")
    cur_tab.execute("commit")

#如果表里所有Regstat，说明已经跑完，重新把 regstat设为0，重新进行测
cur_tab.execute("select id,name, prov, city, ipv4, ipv6 from 3main_node ") ;  
# all available probe
lines = cur_tab.fetchall()
i = 0
#读出表里的所有node
#idxset=list(rang(len(lines)))
#random.shuffle(idxset)
while cur_tab.execute("select id, name, prov, city, ipv4, ipv6 from 3main_node where regstat='0' order by rand() limit 1"):
    line = cur_tab.fetchone();
    excpt=''
    try :
       cur_tab.execute("update v6view set regstat='1' where id= %d" % line[0])       
    except Exception as e :
        print "mysql update error： %s" % e
        excpt='ex'
    finally: 
         cur_tab.execute("commit")
    if excpt=='ex' :
        continue
    #读出的节点设regstat设为1
    for i in range(len(lines)):
        print i
        if line[0] != lines[i][0]: #不ping自己，ping id不同的node               
            if version == '4':
                para1 = line[4];  # source ipv4addr
            else:
                para1 = line[5];
                # source ipv6 addr
            para2 = lines[i][4];  # destination ipv4 addr
            para3 = lines[i][5];  # destination ipv6 addr
        else:
            continue
        #print line[0], i;
        result = ''
        if version == '6':
            cmd = 'http://[' + para1 + ']:9050/ping/pingPop?' + 'ipv4=' + para2 + '&' + 'ipv6=' + para3 + '&count=20';
        else:
            cmd = 'http://' + para1 + ':9050/ping/pingPop?' + 'ipv4=' + para2 + '&' + 'ipv6=' + para3 + '&count=20'
        print "the http commd: %s" % cmd
        # when utilising urllib2 the "\"will not put before "&"
        result = connect_remote(cmd)
        result = json.loads(result)
        print "return result: %s" % result        
        if result.get('code') == '0': #测试错误结果处理
            result = '{"code":"0","resultObject":{"ipv4Delay":"0","ipv4MinDelay":"0","ipv4MaxDelay":"0","ipv4DouDong":"0","ipv6Lost":"0","ipv6MinDelay":"0", \
             "ipv6MaxDelay":"0","ipv4Lost":"0","ipv6Delay":"0","ipv6DouDong":"0.0"}}'
            result = json.loads(result)
        rsltObj = result.get('resultObject')
        if rsltObj.get('ipv6Lost') == '100':
            rsltObj['ipv6DouDong'] = '0'
        if rsltObj.get('ipv4Lost') == '100':
            rsltObj['ipv4DouDong'] = '0'
        item = (line[1], lines[i][1], datetime.datetime.today().isoformat(), result.get('code'),
                float(rsltObj.get('ipv4Delay')),
                float(rsltObj.get('ipv4DouDong')), float(rsltObj.get('ipv4Lost')), float(rsltObj.get('ipv6Delay')),
                float(rsltObj.get('ipv6DouDong')),
                float(rsltObj.get('ipv6Lost')))
        try :
            cur_tab.execute("insert into test6(ori, des, date, code, ipv4delay, ipv4doudong, ipv4lost, ipv6delay,ipv6doudong, ipv6lost) \
              values('%s','%s','%s','%s',%f,%f,%f,%f,%f,%f) " % item)
        except Exception as e:
                    print e
        finally :
               cur_tab.execute("commit")        
            
            #cur_tab.execute("insert into test(ori, des, date, code, ipv4delay, ipv4doudong, ipv4lost, ipv6delay,ipv6doudong, ipv6lost) \
            #    values('%s','%s','%s','%s',%f,%f,%f,%f,%f,%f) " % item)
            
    i = 0
cur_tab.close()
tabl.close()


