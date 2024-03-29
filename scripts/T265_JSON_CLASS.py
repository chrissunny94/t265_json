#!/usr/bin/env python3
import rospy
import rospkg
from std_msgs.msg import Int64 ,Bool
from std_srvs.srv import SetBool
import csv
import os
import math


import json
from datetime import datetime
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from t265_json.msg import JSON
data = json

import socket


rospack = rospkg.RosPack()
Package_Path=rospack.get_path('t265_json')
print ("PackagePath:",Package_Path)
print("CLASS FOR T265")

class T265Json():

    def __init__(self):
        print("Class constructor")
        print("callback for odometry ")
        self.odometry_subscriber = rospy.Subscriber('/android/odom', Odometry, self.callback_t265)
        print("callback for JSON_from_phone")
        self.JSON_subscriber = rospy.Subscriber('/JSON_from_phone', JSON, self.callback_JSON)
        self.Trigger_publisher = rospy.Publisher('/android_call_trigger',Bool, queue_size=10)
        self.Mappingstatus_subscriber = rospy.Subscriber("/MAPPING_STATUS",Bool, self.mappingstatus_callback)
        #self.create_csv(self)
       
        
        
        print("T265 JSON CLASS INITIATED")
        self.MAP_FILE_NAME = 'user_data.csv'
        self.last_time = None
        self.current_time = 0
        self.last_odom = Odometry()
        self.TIME_BASED_TRIGGER = False
        self.DISTANCE_BASED_TRIGGER = False
        self.MAPPING_STATUS= False

    def mappingstatus_callback(self,data):
        print("Mapping Off for ,"+self.MAP_FILE_NAME)
        self.MAPPING_STATUS = data.data

    

    def callback_t265(self,data):
         
        now = datetime.now()
        self.current_time = now.strftime("%H:%M:%S")
        #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.pose.pose.position.x)
        #self.append_csv(data)
        if(self.MAPPING_STATUS):
            if (self.TIME_BASED_TRIGGER ) :
                if (self.last_time == None):
                    #self.last_time = self.current_time
                    self.last_time = now
                    self.current_time = now
                    self.append_csv(data)
                    
                    print("Time based trigger")
                elif ((now - self.last_time).seconds >= 1) :
                    print((now - self.last_time).seconds)
                    self.last_time = now
                    self.append_csv(data)
            elif (self.DISTANCE_BASED_TRIGGER ) :
                X = data.pose.pose.position.x
                Y = data.pose.pose.position.y
                last_x = self.last_odom.pose.pose.position.x
                last_y = self.last_odom.pose.pose.position.y
                if (self.last_odom == None) :
                    self.last_odom = data
                    self.append_csv(data)
                    
                    print("Distance based trigger")
                elif (math.hypot((last_x - X), (last_y - Y)) > .5):
                    self.last_odom = data
                    self.append_csv(data)

   
        
    def callback_JSON(self,data):
        self.MAP_FILE_NAME= data.MAP_NAME+"-" +self.current_time + '.csv'
        self.TIME_BASED_TRIGGER = data.TIME_BASED_TRIGGER
        self.DISTANCE_BASED_TRIGGER = data.DISTANCE_BASED_TRIGGER
        print(data)
        self.create_csv(data)

    def send_JSON(self,data):
        JSON_OBJECT = { "X": str(round(data.pose.pose.position.x,4)), "Y": str(round(data.pose.pose.position.y,4)), "Timestamp":self.current_time}
        send_message(json.dumps(JSON_OBJECT, sort_keys=True, indent= 3))
    
    def create_csv(self,data):
        print("CSV Working")
        with open(Package_Path+'/output/'+self.MAP_FILE_NAME, mode='w') as file:
            
            user_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            user_writer.writerow(['Mapname',data.MAP_NAME])
            user_writer.writerow(['last_location'])
            user_writer.writerow(['Who is creating the Map',data.MAP_CREATOR])
            user_writer.writerow(['GPS_LAT',data.GPS_LAT])
            user_writer.writerow(['GPS_LONG',data.GPS_LONG])
            user_writer.writerow(['calling number',data.calling_number])
            user_writer.writerow(['call duration',data.call_duration])
            user_writer.writerow(['Time-based Trigger',int(data.TIME_BASED_TRIGGER)])
            user_writer.writerow(['Distance-based Trigger',int(data.DISTANCE_BASED_TRIGGER)])
            user_writer.writerow(['X', 'Y', 'Timestamp'])
        print(file.mode)
        self.last_odom = Odometry()
        self.last_time = None

    def append_csv(self,data):
        self.Trigger_publisher.publish(True)
        fields=[str(round(data.pose.pose.position.x,4)),str(round(data.pose.pose.position.y,4)),self.current_time]
        with open(Package_Path+'/output/'+self.MAP_FILE_NAME, 'a+') as f:
            print(fields)
            writer = csv.writer(f)
            writer.writerow(fields)
                
        print("Data appended")


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
