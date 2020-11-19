#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int64
from std_srvs.srv import SetBool



import json
from datetime import datetime
from nav_msgs.msg import Odometry
from std_msgs.msg import String


import socket
import json

print("CLASS FOR T265")

class T265Json():

    def __init__(self):
        print("Class constructor")
        self.odometry_subscriber = rospy.Subscriber('/camera/odom/sample', Odometry, self.callback_t265)
        print("callback for odometry ")

        
        HOST = '127.0.0.1'  # The server's hostname or IP address
        PORT = 8081         # The port used by the server
        print("Setting IP address:",HOST)
        print("Setting PORT:",PORT)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        print("T265 JSON CLASS INITIATED")

    def callback_t265(self,data):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.pose.pose.position.x)
        JSON_OBJECT = { "X": str(round(data.pose.pose.position.x,4)), "Y": str(round(data.pose.pose.position.y,4)), "Timestamp":current_time}
        send_message(json.dumps(JSON_OBJECT, sort_keys=True, indent= 3))


if __name__ == '__main__':
    
    print("main")
    T265Json()
    rospy.init_node('t265_Json_class')
    rospy.spin()