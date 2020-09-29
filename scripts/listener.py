#!/usr/bin/env python

import rospy
import json
from datetime import datetime
from nav_msgs.msg import Odometry
from std_msgs.msg import String


import socket
import json
data = json
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8081         # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def send_message(data):
    s.sendall(data.encode())
    #data = s.recv(1024)


def callback(data):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.pose.pose.position.x)
    JSON_OBJECT = { "X": str(round(data.pose.pose.position.x,4)), "Y": str(round(data.pose.pose.position.y,4)), "Timestamp":current_time}
    send_message(json.dumps(JSON_OBJECT, sort_keys=True, indent= 3))

def listener():

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/camera/odom/sample', Odometry, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
