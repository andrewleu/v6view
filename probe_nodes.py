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

class updatedb (threading.Thread):
    def connect_remote(self, cmmd):
        req = urllib2.Request(cmmd)
        try:
            reslt = urllib2.urlopen(req, data=None, timeout=15)
        except:
            return '500'
        return  reslt.getcode()
    def run(self) :
       dbaddr = "127.0.0.1"
       conn=mysql.connect(dbaddr,'ipv6','ipv6bgp','v6view')
       cur=conn.cursor();
       mutex.acquire()
       try :
         if not cur.execute("select id from v6view where regstat='1'") :
             cur.execute("update v6view set regstat='1'")
       except Exception as e :
             print e 
       finally :
          mutex.release()    
       while 1 :
           mutex.acquire()
           if  not cur.execute("select id, ipv4, ipv6, httpstat from v6view where regstat='1' order by rand() limit 1") :
                 mutex.release()
                 break
           item=cur.fetchone(); err=""
           try :
                cur.execute("update v6view set regstat='0' where id=%d" % item[0])
                cur.execute("commit")
           except Exception as err :
                print err
           finally :
                mutex.release()
           if err !='' :
                continue
           addr=item[1]
           cmd = 'http://' + addr + ':9050/'+'site/domainARecord?website=www.qq.com'
           result=self.connect_remote(cmd); print "%s, addr=%s,  %s" %  (result, addr, item[0])
           cur.execute("update v6view set httpstat='%s'where id='%s'" % (result,item[0]))
           cur.execute("commit")
       print self 
       cur.close()
       conn.close()
       return 1


global mutex
mutex=threading.Lock()
n=8
threads=[]
startTime=int(time.time())
for thrd in range(n) :
    try :
	th=updatedb()
        print th
        threads.append(th)
	th.start()
    except:
       sleep(10)
#   del rfile
       print "Exception occurs"
for th in threads :
   try :
      print th
      th.join()
      time.sleep(5)
   finally :
      print "end" 
endTime=int(time.time())
print "Duration %s"  % (endTime-startTime)
exit(0)


"""

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
        
        print result; #fp.write(str(result)+'\r')
        cur_tab.execute("insert nodestatus(id, result) value(%d,'%s' )" % (node[0], result)) 
        print " "
        cur_tab.execute("commit")
fp.close()		
cur_tab.close()
tabl.close()

"""
