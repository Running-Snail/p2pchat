import server
import client
import threading

def start_server(port):
    s = server.P2PChatServer(port)
    while 1:
        s.recv()
    s.close()

def client_loop(cli):
    print 'start recv loop'
    while 1:
        cli.recv()

def start_client(remote, port):
    c = client.P2PChatClient(remote, port)
    t = threading.Thread(target=client_loop, args=(c,))
    c.register()
    t.start()
    t.join()
    c.close()

def main():
    while 1:
        try:
            command = raw_input('>> ')
            if command.startswith('server'):
                parts = command.split(' ')
                start_server(int(parts[1]))
            elif command.startswith('client'):
                parts = command.split(' ')
                start_client((parts[1], int(parts[2])), int(parts[3]))
        except KeyboardInterrupt as e:
            continue