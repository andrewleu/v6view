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
global mutex, nodes,version
global dbaddr, username,userpass
mutex=threading.Lock()
class updatedb(threading.Thread) :
  def connect_remote(self, cmmd):
    req = urllib2.Request(cmmd)
    try:
        reslt = urllib2.urlopen(req, data=None, timeout=15)
        return reslt.read()
    except Exception as e:
        return e
  def run(self) :
      sys.setdefaultencoding("utf8")
      tabl_sub = mysql.connect(dbaddr, username, userpass, 'v6view', charset='utf8')
      cur_tab_sub = tabl_sub.cursor();
#fp=open("log",'wb')
      cur_tab_sub.execute("set names 'utf8'");  #
      while 1 :
        error=''
        mutex.acquire() 
        try :
              node = nodes[-1]
              del nodes[-1] ;# cur the tail
        except Exception as e :
              error= e 
              print e 
        finally :
             mutex.release()
        if error :
           break
        url = "www.qq.com";i=0
        if version == '4':
                para1 = node[2];  # source ipv4addr
        else:
                para1 = node[3];
                # source ipv6 addr
        para2 = url
        print node ; #fp.write(str(node))
        ports =["9050","33033"]
        for port in ports :
          if version == '6':
                cmd = 'http://[' + para1 + ']:'+port+'/'
          else:
                cmd = 'http://' + para1 + ':'+port+'/';  # /site/domainARecord?website=+para2
          req = cmd + 'site/homePage?website=' + para2 + '&status=0&ipstatus=4'
          result=self.connect_remote(req)
          print "return result %s" %  result; #fp.write(str(result)+'\r')
          cur_tab_sub.execute("insert nodestatus(id, result,port) value(%d,'%s',%d )" % (node[0], result, int(port))) 
          cur_tab_sub.execute("commit")            
      cur_tab_sub.close()
      tabl_sub.close()


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
nodes= list(cur_tab.fetchall())
cur_tab.execute("truncate nodestatus")
n=5
threads=[]
startTime=int(time.time())
for thrd in range(n) :
    try :
      	th=updatedb()
        print th
        threads.append(th)
        th.start()
    except Exception as e :
       sleep(10)
#   del rfile
       print e
for th in threads :
   try :
      print th
      th.join()
      time.sleep(5)
   finally :
      print "end" 
endTime=int(time.time())
print "Duration %s"  % (endTime-startTime)
cur_tab.execute("update v6view set httpstat='500' ")
cur_tab.execute("commit")
cur_tab.execute("update v6view, nodestatus set v6view.httpstat='200', v6view.port=nodestatus.port where nodestatus.id=v6view.id and nodestatus.result regexp '^[1-9][0-9]*$'")
cur_tab.execute("update v6view, nodestatus set v6view.httpstat='201', v6view.port=nodestatus.port where nodestatus.id=v6view.id and nodestatus.result regexp '^[1-9][0-9]{0,2}[.][0-9]+'") 
cur_tab.execute("update v6view, nodestatus set v6view.httpstat='202', v6view.port=nodestatus.port where nodestatus.id=v6view.id and nodestatus.result like 'HTTP%'")
cur_tab.execute("commit")
cur_tab.close()
tabl.close()

