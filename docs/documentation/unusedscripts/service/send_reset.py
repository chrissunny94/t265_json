#!/usr/bin/env python

import rospy
import json

import socket
data = json
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8080         # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def send_message(data):
    s.sendall(data.encode())
    #data = s.recv(1024)

reset = bool
reset = True
def send_msg(data):
    JSON_OBJECT = { "Reset ": reset}
    send_message(json.dumps(JSON_OBJECT, sort_keys = True))

#s.close()

def listener():
    rospy.init_node('listener', anonymous=True)
    send_msg(data)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
