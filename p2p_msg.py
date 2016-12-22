import json

def _serialize(obj):
    return json.dumps(obj)

def unserialize(msg):
    return json.loads(msg)

def register_msg(device_id, private_addr):
    return _serialize({
        'action': 'register',
        'device_id': device_id,
        'private_addr': private_addr,
    })

def connect_msg(device_id):
    return _serialize({
        'action': 'connect',
        'device_id': device_id
    })

def text_msg(text):
    return _serialize({
        'action': 'text',
        'text': text
    })

def response_connect_msg(device_id, public_addr):
    return _serialize({
        'action': 'response.connect',
        'device_id': device_id,
        'public_addr': public_addr
    })
