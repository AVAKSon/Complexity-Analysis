
import socket
ips = set(i[4][0] for i in socket.getaddrinfo('www.kame.net', 80))
for ip in ips: print ip
