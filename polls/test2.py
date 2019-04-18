
import socket, json
import subprocess

ip_port = ('192.168.10.40', 7000)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ip_port)
s.listen(5)

def pack_cmd_header(header, size):
    bytes_header = json.dumps(header).encode('utf-8')
    fill_size = size - len(bytes_header)
    print('need to fill:', fill_size)
    header['fill'] = header['fill'].zfill(fill_size)
    print('new header fill: ' , header['fill'])
    new_bytes_header =  json.dumps(header).encode('utf-8')
    print("head size:", len(new_bytes_header))
    return new_bytes_header


while True:
    conn, addr = s.accept()
    print('client IP:', addr)

    while True:
        cmd = conn.recv(1024)
        if len(cmd) == 0 :
            break
        print('recv cmd', cmd.decode('utf-8'))

        res = subprocess.Popen(cmd.decode('utf-8'), shell=True,
                               stdout = subprocess.PIPE,
                               stdin = subprocess.PIPE,
                               stderr = subprocess.PIPE
                               )
        stderr = res.stderr.read()
        stdout = res.stdout.read()
        ret = stderr + stdout
        data_length = len(ret)
        print('the length of the data: ' + str(data_length))
        header_data = {'length': data_length,
                       'fill':''
                       }
        header = pack_cmd_header(header_data, 100)
        conn.send(header)
        conn.send(ret)

    conn.close()
