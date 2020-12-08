#!/usr/bin/env python3

import socket
import os
from t265_json.msg import JSON
from std_msgs.msg import Float32
import rospy
import json
import sys

HOST = '192.168.1.16'  # Standard loopback interface address (localhost)
PORT = 8081        # Port to listen on (non-privileged ports are > 1023)

os.system('fuser -$SIGNAL_NUMBER_OR_NAME -kn tcp 8081')
os.system('fuser -n tcp 8081')

hostname = socket.gethostname()
print("Your Computer Name is:" + hostname)    
HOST = str(os.popen('hostname -I').read())
HOST = HOST.replace("\n","")
HOST = HOST.replace(" ","")

print("Your Computer IP Address is:",HOST)  
PORT = 8081
print("Port:",PORT)




#self.pub_JSON(temp_variable)
pub_JSON = rospy.Publisher('/JSON_from_phone', JSON, queue_size=1)                
rospy.init_node('JSON_server_simple', anonymous=True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        try:
            while True:
                data = str(conn.recv(1024))
                print(data.find('map_name'), len(data))
                JSON_string = data[(data.find('map_name')-2):(len(data)-1)]
                print(JSON_string)
                JSON_data = json.loads(JSON_string)
                temp_variable = JSON()
                temp_variable.MAP_NAME=              str(JSON_data['map_name']).replace("\"","")
                temp_variable.MAP_CREATOR=           str(JSON_data['who_is_creating_the_map'])
                #temp_variable.GPS_LAT=               (JSON_data['last_location']['latitude'])
                #temp_variable.GPS_LONG=              (JSON_data['last_location']['longitude'])
                temp_variable.calling_number=        (JSON_data['calling_number'])
                #temp_variable.call_duration=         (JSON_data['call_duration'])
                temp_variable.TIME_BASED_TRIGGER=    (JSON_data['time_based_trigger'])
                #temp_variable.DISTANCE_BASED_TRIGGER=(JSON_data['distance_based_trigger'])
                print(temp_variable)
                pub_JSON.publish(temp_variable)
            
        except KeyboardInterrupt:
            print('interrupted!')
            s.close()
            