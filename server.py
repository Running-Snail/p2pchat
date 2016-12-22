import socket

import p2p_msg
import util
import pprint


class P2PChatServer(object):
    def __init__(self, port):
        self.port = port
        self.setup()
    
    def setup(self):
        self.ip = util.get_ip()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((self.ip, self.port))
        print 'server at', (self.ip, self.port)

        self.clients = {}

    def _send_client(self, addr, msg):
        self._sock.sendto(msg, addr)

    def recv(self):
        msg, addr = self._sock.recvfrom(1024)
        print 'recv', msg, 'from', addr
        data = p2p_msg.unserialize(msg)
        if data['action'] == 'register':
            self.clients[data['device_id']] = {
                'private_addr': data['private_addr'],
                'device_id': data['device_id'],
                'public_addr': addr
            }
            print 'current clients', self.clients
        elif data['action'] == 'connect':
            if data['device_id'] in self.clients:
                public_addr = self.clients[data['device_id']]['public_addr']
                resp = p2p_msg.response_connect_msg(
                    data['device_id'], public_addr
                )
                self._send_client(addr, resp)
    
    def list(self):
        pprint.pprint(self.clients)
    
    def close(self):
        if self._sock is not None:
            self._sock.close()
