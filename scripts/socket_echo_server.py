#!/usr/bin/env python3


import socket
import sys , os
from t265_json.msg import JSON
import rospy
import json
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port

os.system('fuser -$SIGNAL_NUMBER_OR_NAME -kn tcp 8081')
os.system('fuser -n tcp 8081')
os.system('kill -9 $(lsof -i:8081 -t)')

hostname = socket.gethostname()
print("Your Computer Name is:" + hostname)    
HOST = str(os.popen('hostname -I').read())
HOST = HOST.replace("\n","")
HOST = HOST.replace(" ","")

print("Your Computer IP Address is:",HOST)  
PORT = 8081
print("Port:",PORT)

server_address = (HOST, PORT)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

pub_JSON = rospy.Publisher('/JSON_from_phone', JSON, queue_size=1)                
rospy.init_node('JSON_server_simple', anonymous=True)


while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = (connection.recv(1048))
            #print('received {!r}'.format(data))
            
            #print(JSON_string)
            
            if data:
                print('sending data back to the client')
                connection.sendall(data)
                data = str(data)
                JSON_string = data[(data.find('map_name')-2):(len(data)-1)]
                JSON_data = json.loads(JSON_string)
                temp_variable = JSON()
                temp_variable.MAP_NAME              = (JSON_data['map_name'])
                temp_variable.MAP_CREATOR           = (JSON_data['who_is_creating_the_map'])
                temp_variable.GPS_LAT               = (JSON_data['last_location']['latitude'])
                temp_variable.GPS_LONG              = (JSON_data['last_location']['longitude'])
                temp_variable.calling_number        = (JSON_data['calling_number'])
                temp_variable.call_duration         = (JSON_data['call_duration'])
                temp_variable.TIME_BASED_TRIGGER    = (JSON_data['time_based_trigger'])
                temp_variable.DISTANCE_BASED_TRIGGER= (JSON_data['distance_based_trigger'])
                print(temp_variable)
                pub_JSON.publish(temp_variable)
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()

