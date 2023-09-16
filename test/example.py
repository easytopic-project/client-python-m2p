import sys, os.path
modules_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+ '/src/')
sys.path.append(modules_dir)

from client_python_m2p import M2P

import os
import json

f = open(os.path.dirname(__file__) + '/module-name-specs.json')
specs = json.load(f)

QUEUE_SERVER_HOST, QUEUE_SERVER_PORT = os.environ.get(
    "QUEUE_SERVER", "localhost:3002").split(":")

def myCode(msg):

    print(msg)
    
    msg["echo-image"] = msg["input-image"]
    msg["echo-video"] = msg["input-video"]
    msg["backwords-text"] = msg["input-text"][::-1]

    return msg

MyM2P = M2P(QUEUE_SERVER_HOST, QUEUE_SERVER_PORT, specs, myCode)

MyM2P.connect()

MyM2P.run()