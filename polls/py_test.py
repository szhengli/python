import socket
import subprocess
import json

ip_port = ('192.168.10.132', 7000)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

res = s.connect_ex(ip_port)

while True:
    cmd = input('>>:').strip()
    if len(cmd) == 0 : continue
    if cmd  == 'quit': break
    s.send(cmd.encode('utf-8'))

    header = json.loads(s.recv(100).decode('utf-8'))
    length = header['length']
    data = b''
    data_len=0
    while  data_len < length
        data += s.recv(1024)
        data_len = len(data)
    response = data.decode('utf-8')

    print(response)
    print("length:" + str(length))
    print('response length:' , str(len(response)))
    print('data length:', str(len(data)))
