import socket
import ssl

target_host = "www.google.com"
target_port = 443

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))
client = ssl.wrap_socket(client, keyfile=None, certfile=None,
                        server_side=False, cert_reqs=ssl.CERT_NONE,
                                        ssl_version=ssl.PROTOCOL_TLSv1_2)

client.send(b"GET / HTTP/1.1\r\nHOST: google.com\r\n\r\n")

while True:
  res = client.recv(4096)
  print(res)
  if len(res) < 4096:
    break
