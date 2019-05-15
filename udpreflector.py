import socket
s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
s.bind(('',6910))
r= socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
print( "this python prog can recieve udp packets sent to port 6910")
print("and sent those packets back to the origin IPv6 address with destination port 31000")


while True :
    data, addr = s.recvfrom(2048)
    if data==' ':
        print "client has exist"
    if data :
        address= (addr[0], 31000)
        r.sendto(data,address)
        print "received:", data, "from", addr
s.close()
r.close()

