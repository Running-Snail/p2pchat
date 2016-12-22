import client
import threading

def loop(cli):
    print 'start recv loop'
    while 1:
        cli.recv()

def main():
    c = client.P2PChatClient(('192.168.31.136', 51515), 52525)
    t = threading.Thread(target=loop, args=(c,))
    
    c.register()
    t.start()
    t.join()
    c.close()

if __name__ == '__main__':
    main()
