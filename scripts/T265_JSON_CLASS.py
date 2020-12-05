#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int64
from std_srvs.srv import SetBool
import csv
import os


import json
from datetime import datetime
from nav_msgs.msg import Odometry
from std_msgs.msg import String
data = json

import socket
import json

print("CLASS FOR T265")

class T265Json():

    def __init__(self):
        print("Class constructor")
        self.odometry_subscriber = rospy.Subscriber('/camera/odom/sample', Odometry, self.callback_t265)
        print("callback for odometry ")
        
        #self.create_csv(self)
       
        self.current_time = 0

        HOST = '127.0.0.1'  # The server's hostname or IP address
        PORT = 8082         # The port used by the server
        print("Setting IP address:",HOST)
        print("Setting PORT:",PORT)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        print("T265 JSON CLASS INITIATED")

    def callback_t265(self,data):
        now = datetime.now()
        self.current_time = now.strftime("%H:%M:%S")
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.pose.pose.position.x)
        self.create_csv(data)
        self.create_csv2(data)
        #self.append(data)
        

    def send_JSON(self,data):
        JSON_OBJECT = { "X": str(round(data.pose.pose.position.x,4)), "Y": str(round(data.pose.pose.position.y,4)), "Timestamp":current_time}
        send_message(json.dumps(JSON_OBJECT, sort_keys=True, indent= 3))
    
    def create_csv(self,data):
        print("CSV Working")
        with open('user_data.csv', mode='w') as file:
            
            user_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            user_writer.writerow(['Mapname'])
            user_writer.writerow(['Who is creating the Map'])
            user_writer.writerow(['calling number'])
            user_writer.writerow(['call duration'])
            user_writer.writerow(['last_location'])
            user_writer.writerow(['Time-based Trigger'])
            user_writer.writerow(['Distance-based Trigger'])
            user_writer.writerow(['X', 'Y', 'Timestamp'])
        print(file.mode)

    def create_csv2(self,data):
        fields=[str(round(data.pose.pose.position.x,4)),str(round(data.pose.pose.position.y,4)),self.current_time]
        with open('user_data.csv', 'a+') as f:
            #line = f.readline()
            
            #for line in f:
                    #line = f.readline()
                    #writer.writerow(fields)
                    #print(fields)
                   
            print(fields)
            writer = csv.writer(f)
            writer.writerow(fields)
                
        print(f.mode)

    def append(self,data):
        print("append working")
        fieldnames = ['X','Y','Timestamp']
        with open('user_data.csv', 'a') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerow({'X':str(round(data.pose.pose.position.x,4)), 'Y':str(round(data.pose.pose.position.y,4)), "Timestamp":self.current_time})

if __name__ == '__main__':
    
    print("main")
    T265Json()
    rospy.init_node('t265_Json_class')
    rospy.spin()