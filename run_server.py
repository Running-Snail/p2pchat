import server

def main():
    s = server.P2PChatServer(51515)
    while 1:
        s.recv()
    s.close()

if __name__ == '__main__':
    main()
