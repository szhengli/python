import subprocess, time
import socketio
sio=socketio.Client()
sio.connect('http://localhost:5000')

out=subprocess.Popen(' tail -f  /root/t.txt ', shell=True, bufsize=0 ,  stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
while True:
    try:
        l=out.readline().decode()
        print(l)
        sio.emit('pub',l)
        if  'ends' in l :
            break
    except:
        sio.disconnect()
        break

