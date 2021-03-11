#!/usr/bin/env python3
import rospy, rospkg
from std_msgs.msg import Int64 ,Bool
from std_srvs.srv import SetBool
import csv
import os
import math
import socket
import json
from datetime import datetime
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from t265_json.msg import JSON
import sys , os
import time

import asyncio



BUFSIZE=1096

rospack = rospkg.RosPack()
Package_Path=rospack.get_path('t265_json')
print ("PackagePath:",Package_Path)
print("CLASS FOR T265")


# Create a TCP/IP socket
# Bind the socket to the port

os.system('fuser -$SIGNAL_NUMBER_OR_NAME -kn tcp 8081')
os.system('fuser -n tcp 8081')
#os.system('kill -9 $(lsof -i:8081 -t)')



class T265JsonServer():

    def __init__(self):
        print("Class constructor")
        self.pub_JSON = rospy.Publisher('/JSON_from_phone', JSON, queue_size=1)  
        self.Trigger_sub = rospy.Subscriber('/android_call_trigger',Bool,self.trigger_callback)
              
        self.trigger_bool = False

        
        
        self.current_time = 0

        hostname = socket.gethostname()
        print("Your Computer Name is:" + hostname)    
        HOST = str(os.popen('hostname -I').read())
        HOST = HOST.replace("\n","")
        HOST = HOST.replace(" ","")
        self.HOST = HOST


        PORT = 8083         # The port used by the server
        self.PORT = PORT
        print("Setting IP address:",self.HOST)
        print("Setting PORT:",self.PORT)
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None


        print("T265 JSON CLASS INITIATED")
        
        self.socket_loop_function()
        self.temp_variable = JSON()
                
    
    def trigger_callback(self,data):
        print("trigger recieved")
        self.trigger_bool = True
        
    def Out_pub_JSON(self,data):
        self.pub_JSON.publish(data)



    def socket_loop_function(self):
        try:
            print("\nSocket")
            self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(1)
            self.client.setblocking(0)
            self.client.bind((self.HOST, self.PORT))
            self.client.listen(1) # how many connections can it receive at one time
            print ("Start Listening...")
            while not rospy.is_shutdown():
                try:
                    self.client.settimeout(None)
                    conn, addr = self.client.accept()
                    print ("client with address: ", addr, " is connected.")
                    #conn.settimeout(None)
                    conn.setblocking(0)
                    data=conn.recv(BUFSIZE).decode()
                    JSON_data = json.loads(data)
                    print ("Recieved this data: <", JSON_data, "> from the client.")
                except :
                    JSON_data = {"BLANK":True}
                    #conn = False

                if(conn ):
                    print("\nCOnnection established")
                    if(self.trigger_bool):
                        #self.client.settimeout(20)
                        ack_packet = json.dumps({"trigger_call":True})
                        print('\n\n\nsending data back to the client\n\n'+ack_packet)
                        conn.sendall(ack_packet.encode("utf-8"))
                        self.trigger_bool = False
                    
                    if ('BLANK' not in JSON_data):
                        if 'map_name' in JSON_data:
                            print(data)
                            print('\nsending data back to the client')
                            ack_packet = 'Data_recieved_by_raspberry_pi'
                            conn.send(ack_packet.encode("utf-8"))
                            print(data)
                            print(JSON_data["map_name"])
                            temp_variable = JSON()
                            temp_variable.MAP_NAME              = str(JSON_data['map_name'])
                            temp_variable.MAP_CREATOR           = str(JSON_data['map_created_by'])
                            temp_variable.GPS_LAT               = float(JSON_data['last_location']['system_latitude'])
                            temp_variable.GPS_LONG              = float(JSON_data['last_location']['system_longitude'])
                            temp_variable.calling_number        = str(JSON_data['calling_number'])
                            temp_variable.call_duration         = float(JSON_data['call_duration'])
                            temp_variable.TIME_BASED_TRIGGER    = (JSON_data['trigger_time_based'])
                            temp_variable.DISTANCE_BASED_TRIGGER= (JSON_data['trigger_distance_based'])
                            print(temp_variable)
                            self.Out_pub_JSON(temp_variable)
                            print ("x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x")
                            
                        
                        elif 'stop_mapping' in JSON_data:
                            print("stop mapping ")
                            ack_packet = json.dumps({"stopped_mapping":True})
                            print('\n\n\nsending data back to the client\n\n'+ack_packet)
                            conn.send(ack_packet.encode("utf-8"))
                    else:
                        time.sleep(1)
                        print('\nNODATA')
                elif(not conn):
                    print("\nNo connection")
                    pass
                    
            self.client.close()
        except KeyboardInterrupt:
            self.client.close()
    


    
if __name__ == '__main__':
    
    rospy.init_node('socket_server')
    
    print("main")
    T265JsonServer()
    rospy.spin()
        
    





