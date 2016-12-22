import socket
from uuid import getnode as get_mac

import p2p_msg
import util


class P2PChatClient(object):
    def __init__(self, remote, port):
        self.private_port = port
        # remote = (ip, port)
        self.remote = remote
        self.setup()

    def setup(self):
        self.device_id = str(get_mac())
        self.private_ip = util.get_ip()
        self.private_addr = (self.private_ip, self.private_port)
        self.peer = {}

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(self.private_addr)
        self._connect_cb = None

    def _send_remote(self, msg):
        self._sock.sendto(msg, self.remote)
    
    def _send_peer(self, addr, msg):
        self._sock.sendto(msg, addr)
    
    def recv(self):
        msg, addr = self._sock.recvfrom(1024)
        print 'recv', msg, 'from', addr
        data = p2p_msg.unserialize(msg)
        if data['action'] == 'response.connect':
            if 'error' in data:
                print 'error', data['error']
            else:
                device_id = data['device_id']
                peer_public_addr = data['public_addr']
                print 'peer_public_addr', peer_public_addr
                self.peer[device_id] = {
                    'public_addr': (peer_public_addr[0], peer_public_addr[1])
                }
                if self._connect_cb is not None:
                    self._connect_cb(self, device_id)

    def register(self):
        print 'begin to register'
        msg = p2p_msg.register_msg(
            self.device_id,
            self.private_addr
        )
        self._send_remote(msg)
    
    def connect(self, device_id, cb):
        msg = p2p_msg.connect_msg(device_id)
        self._send_remote(msg)
        self._connect_cb = cb
    
    def send(self, device_id, text):
        msg = p2p_msg.text_msg(text)
        peer_public_addr = self.peer[device_id]['public_addr']
        print 'peer_public_addr', peer_public_addr
        self._send_peer(peer_public_addr, msg)

    def close(self):
        if self._sock is not None:
            self._sock.close()
