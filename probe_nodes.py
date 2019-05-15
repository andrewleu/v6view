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
