import client
import threading

def loop(cli):
    print 'start recv loop'
    while 1:
        cli.recv()

def connected(cli, device_id):
    print 'connected', device_id
    cli.send(device_id, 'hello')

def main():
    c = client.P2PChatClient(('192.168.31.136', 51515), 52526)
    c.device_id = 'ttttt'
    t = threading.Thread(target=loop, args=(c,))
    t.start()

    c.register()
    c.connect('30902514630318', connected)

    t.join()
    c.close()

if __name__ == '__main__':
    main()
