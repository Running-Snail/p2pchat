import socket

def main():
    host = '192.168.31.136'
    port = 51423
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((host, port))
    s.sendall('hello')
    msg, addr = s.recvfrom(1024)
    print 'got ', msg, 'from', addr
    s.close()

if __name__ == '__main__':
    main()
