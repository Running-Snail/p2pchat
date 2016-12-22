import server
import client
import threading
import time
import sys
import os
import signal

sobj = None
cobj = None
peer_id = None
pause = False

def start_server(port):
    global sobj
    sobj = server.P2PChatServer(port)
    print 'start reciving'
    while 1:
        sobj.recv()
    sobj.close()

def server_command(port):
    port = int(port)
    t = threading.Thread(target=start_server, args=(port, ))
    t.daemon = True
    t.start()

def start_client(remote, port):
    global cobj
    cobj = client.P2PChatClient(remote, port)
    while 1:
        cobj.recv()
    cobj.close()

def client_command(remote_ip, remote_port, port):
    remote_port = int(remote_port)
    port = int(port)
    t = threading.Thread(target=start_client, args=((remote_ip, remote_port), port))
    t.daemon = True
    t.start()

def register_command():
    global cobj
    if cobj is not None:
        cobj.register()
    else:
        print 'no client'

def connect_command(device_id):
    global cobj
    def connected(cli, device_id):
        peer_id = device_id
        pause = False
    
    pause = True
    if cobj is not None:
        cobj.connect(device_id, connected)
    else:
        print 'no client'

def say_command(text):
    global cobj
    if cobj is not None:
        cobj.send(peer_id, text)
    else:
        print 'no client'

def list_command():
    global sobj
    if sobj is not None:
        sobj.list()
    else:
        print 'no server'

def exit_command():
    if sobj is not None:
        sobj.close()
    if cobj is not None:
        cobj.close()
    print 'bye'
    sys.exit(0)

handlers = {
    'server': server_command,
    'client': client_command,
    'register': register_command,
    'connect': connect_command,
    'say': say_command,
    'list': list_command,
    'exit': exit_command
}

def signal_handler(signal, frame):
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    while 1:
        while pause:
            time.sleep(0.2)
        try:
            command = raw_input('>> ')
        except EOFError as e:
            print 'bye'
            break
        parts = command.split(' ')
        action = parts[0]
        if action in handlers:
            handlers[action](*parts[1:])

if __name__ == '__main__':
    main()
