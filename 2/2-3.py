import socket

buffer_size = 4096
target_host = "127.0.0.1"
target_port = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"AAABBBCCC", (target_host, target_port))

data, addr = client.recvfrom(buffer_size)

print("[*] Receive:{} from {}:{}".format(data.decode('utf-8').strip(), addr[0], addr[1]))