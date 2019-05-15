# -*- coding: UTF-8 -*-
# this scipt is to control the remote nodes to resolve web addr 
# and to access some website,  Version 3
# import sqlite3
import datetime
# import os
import json
import sys
import urllib2
import MySQLdb as mysql
from sys import argv
import time
global cur_tab


def webprobe(ipver, para2,cmd, _entr) :
            req = cmd + 'site/homePage?website=' + para2 + '&status=0&ipstatus='+ipver ; #print req
            result = connect_remote(req)
            _entr.append(ipver); print _entr
            if result == '500':
                result = connect_remote(req);  # try again
                if result == '500':
                    cur_tab.execute("insert webprobe2 set nodename='%s', website='%s' ,code='%s',\
                    ipv4addr='%s', ipv6addr='%s',ipver='%s', acsrate=0, acsdelay=0" % tuple(_entr))
                    cur_tab.execute("commit");
                    _entr.append(' '); # blank for hash 
                    return 0 
            # getting rate and time has errors
            if result !=  '500' :
                retcode=result.read(); e=''
                print retcode 
                mdhashtxt=_entr[0]+_entr[1]+datetime.datetime.now().isoformat() ;#.replace(":","")
                # mdhashtxt=mdhashtxt.encode().replace("-","").decode()
                _entr.append(mdhashtxt)
                try :
                   cur_tab.execute("insert webprobe2 set nodename='%s', website='%s',code='%s', \
                   ipv4addr='%s', ipv6addr='%s',date=(select now()), ipver='%s',\
                   md5hash=(select md5(hex('%s')))" % tuple(_entr)) ; #str to hex then md5
                   cur_tab.execute("insert webresp set  idx='%s', \
                      md5hash=(select md5(hex('%s'))), ipver='%s'" \
                     % ( retcode, mdhashtxt, ipver))
                   if result.getcode()!=200 :
                     cur_tab.execute("commit")
                     cur_tab.execute("update webprobe2 set acsrate=0 , acsdelay=0 \
                     where md5hash=(select md5(hex('%s'))" % md5hashtxt)
                     cur_tab.execute("update webresp set idx =0 where md5hash=(select md5(hex('%s'))" % md5hashtxt)
            # ipv6 website access
                except Exception as e :
                   print e
                finally :
                    cur_tab.execute("commit");
                if e :
                   return 0
                else :
                   return 1
 

def connect_remote(cmmd):
    req = urllib2.Request(cmmd)
    try:
        reslt = urllib2.urlopen(req, data=None, timeout=15)
    except:
        return '500'
    return reslt


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
     # version = '4'
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
#cur_tab.execute("select url, type from urllist");urls = cur_tab.fetchall()
cur_tab.execute("select id, name,  ipv4, ipv6 from 3main_node")
nodes= cur_tab.fetchall()
# fetch all the url in the list
if not cur_tab.execute("select id from urllist where status=0"):
    cur_tab.execute("update urllist set status=0")
    cur_tab.execute("commit")
# 如果表里所有Regstat为1，说明已经跑完，重新把?regstat设为0，重新进行测试
while   cur_tab.execute("select url, type,id from urllist where status=0 order by rand() limit 1" ) :
        url = cur_tab.fetchone();  i=0
        err=0
        try :
          cur_tab.execute("update urllist set status='1' where id= %d" % url[2])
          cur_tab.execute("commit")
        except Exception as e :
           print e
           err=1
        if err==1 :
           continue
        # 读出的节点设regstat设为1
        for i in range(len(nodes)):
            if version == '4':
                para1 = nodes[i][2];  # source ipv4addr
            else:
                para1 = nodes[i][3];
                # source ipv6 addr
            para2 = url[0]
            if version == '6':
                cmd = 'http://[' + para1 + ']:9050/'
            else:
                cmd = 'http://' + para1 + ':9050/';  # /site/domainARecord?website=+para2
            req = cmd + 'site/domainARecord?website=' + para2
            # when utilising urllib2 the "\"will not put before "&"
            result = connect_remote(req)
            entry = [nodes[i][1], url[0]] 
            if result == '500':
                entry.append("500")
                cur_tab.execute("insert webprobe2 set nodename='%s', website='%s',code='%s',date=(select now())" % tuple(entry))
                cur_tab.execute("commit")
                i += 1
                continue
            # the node is not working, skip it, mark code 500
            entry.append(str(result.getcode()))
            entry.append(result.read());  # .replace(',','')) blob
            # get A record
            req = cmd + 'site/domainAAAARecord?website=' + para2
            result = connect_remote(req)
            if result == '500':
                entry.append(",")
            else:
                addr = result.read();  # .split(",")[0] blob
                entry.append(addr)
                # get AAAA record
            if url[1] == 'app':
                i += 1
                cur_tab.execute("insert webprobe2 set nodename='%s', website='%s',code='%s', ipv4addr='%s', \
                                ipv6addr='%s', date=(select now())"
                                % tuple(entry))
                continue
                # for those app type url this step is enough
            webprobe("4",para2,cmd, entry) ; #print entry
            entry=entry[:-2] ;# empty the field for ipver and md5hash
            if  entry[-1]!= ',' : 
                 #the last of the list is ipv6 address
                 webprobe("6",para2,cmd, entry) ; #print entry
while( cur_tab.execute("select md5hash, nodename from webprobe2 where acsrate is null and acsdelay is null and md5hash is not NULL order by rand() limit 1")) :
       md5hash,nodename=cur_tab.fetchone(); err=''; result='';req=''
       print "hash: %s" % md5hash
       if  not cur_tab.execute("select  idx,ipver from webresp where md5hash='%s'" % md5hash):
            err='error'
       else  :
             residx=cur_tab.fetchone()
             if residx[0]=='0' :  
                err='error' ; # idx is 0, dont have to fetch the result
             else :
                 cur_tab.execute("select ipv4 from v6view where name='%s' limit 1" % nodename ) 
                 addr=cur_tab.fetchone()[0]; print addr
                 req = "http://"+addr+":9050" + "/site/getRateAndTime?id="+residx[0]
                 print req
                 result =  connect_remote(req)
       if result == '500' or err=='error' :
                    result = connect_remote(req)
                    if result == '500' or err=='error' :
                       try :
                          cur_tab.execute("update webprobe2 set acsrate=0, acsdelay=0 where md5hash='%s' " % md5hash)
                       except Exception as e :
                          print e
                       finally :
                           cur_tab.execute("commit")
                       continue
       if result != '500' :
           read_result=result.read(); print read_result
           result=json.loads(read_result) 
           try :
                cur_tab.execute("update webprobe2 set acsrate=%f,acsdelay=%f where md5hash='%s'"
                            % (result['rate'],result['time'],md5hash))
                cur_tab.execute("update webresp set result='%s' where md5hash='%s' " % (read_result, md5hash))
           except Exception as e  :
                print e
           finally  :
                cur_tab.execute("commit") 
           continue 
cur_tab.close()
tabl.close()

