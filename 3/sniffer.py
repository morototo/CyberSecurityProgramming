import socket
import os

host = "192.168.11.6"

if os.name == "nt":
  socket_protocol = socket.IPPROTO_IP
else:
  socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))

if os.name == "nt":
  sniffer.setsockopt(socket.IPPROTO_IP, socket.RCVALL_ON)

print sniffer.recvfrom(65565)

if os.name == "nt":
  sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)