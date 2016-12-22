import server
import client
import threading
import time

sobj = None
cobj = None
peer_id = None
pause = False

def start_server(port):
    sobj = server.P2PChatServer(port)
    print 'start reciving'
    while 1:
        sobj.recv()
    sobj.close()

def server_command(port):
    port = int(port)
    t = threading.Thread(target=start_server, args=(port, ))
    t.start()

def start_client(remote, port):
    cobj = client.P2PChatClient(remote, port)
    while 1:
        cobj.recv()
    cobj.close()

def client_command(remote_ip, remote_port, port):
    remote_port = int(remote_port)
    port = int(port)
    t = threading.Thread(target=start_client, args=((remote_ip, remote_port), port))
    t.start()

def register_command():
    if cobj is not None:
        cobj.register()
    else:
        print 'no client'

def connect_command(device_id):
    def connected(cli, device_id):
        peer_id = device_id
        pause = False
    
    pause = True
    if cobj is not None:
        cobj.connect(device_id, connected)
    else:
        print 'no client'

def say_command(text):
    if cobj is not None:
        cobj.send(peer_id, text)
    else:
        print 'no client'

def list_command():
    print sobj
    if sobj is not None:
        sobj.list()
    else:
        print 'no server'

handlers = {
    'server': server_command,
    'client': client_command,
    'register': register_command,
    'connect': connect_command,
    'say': say_command,
    'list': list_command
}

def main():
    while 1:
        while pause:
            time.sleep(0.2)
        command = raw_input('>> ')
        parts = command.split(' ')
        action = parts[0]
        if action in handlers:
            handlers[action](*parts[1:])

if __name__ == '__main__':
    main()
