

#!/usr/bin/env python
import socket
import sys , os
from t265_json.msg import JSON
import rospy
import json
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
#sock.bind(server_address)

# Listen for incoming connections
#sock.listen(1)

pub_JSON = rospy.Publisher('/JSON_from_phone', JSON, queue_size=1)                
rospy.init_node('JSON_server_simple', anonymous=True)


def recv(): 
    try:
        client.bind((HOST, PORT))
    finally:
        pass
    client.listen(10) # how many connections can it receive at one time
    print ("Start Listening...")
    
    while True:
        conn, addr = client.accept()
        print ("client with address: ", addr, " is connected.")
        data = conn.recv(1024)
        print ("Recieved this data: <", data, "> from the client.")

        if data:
            print(data)
            print('\nsending data back to the client')
            ack_packet = 'Data_recieved_by_raspberry_pi'
            conn.sendall(ack_packet.encode("utf-8"))
            print(data)
            #data = str(data)
            #JSON_string = data[(data.find('map_name')-2):(len(data))]
            JSON_data = json.loads(data)
            #JSON_data = json.loads(JSON_string)
            print(JSON_data)
            print(JSON_data["map_name"])
            temp_variable = JSON()
            temp_variable.MAP_NAME              = str(JSON_data['map_name'])
            temp_variable.MAP_CREATOR           = str(JSON_data['who_is_creating_the_map'])
            temp_variable.GPS_LAT               = float(JSON_data['last_location']['system_latitude'])
            temp_variable.GPS_LONG              = float(JSON_data['last_location']['system_longitude'])
            temp_variable.calling_number        = str(JSON_data['calling_number'])
            temp_variable.call_duration         = float(JSON_data['call_duration'])
            temp_variable.TIME_BASED_TRIGGER    = (JSON_data['time_based_trigger'])
            temp_variable.DISTANCE_BASED_TRIGGER= (JSON_data['distance_based_trigger'])
            print(temp_variable)
            pub_JSON.publish(temp_variable)
            print ("x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x")

        
        elif data == "Correct":
            reply = "Success"
            conn.send(reply.encode("utf-8"))
            conn.close()
            print ("-----------------------------")
        elif data == "Disconnect":
            reply = "Disconnected and the listen has Stopped"
            conn.send(reply.encode("utf-8"))
            conn.close()
            break
        else:
            reply = "Failed"
            conn.send(reply.encode("utf-8"))
            conn.close()
            print ("-----------------------------")
            
    client.close()
"""
You can use thread for the recieve operation so that the execution in main thread
isn't wait until complete the recieve operation. 
"""
#thread = threading.Thread(target = recvFromAndroid, args = ())
#thread.start()
recv()
print( "completed")


# while True:
#     # Wait for a connection
#     print('waiting for a connection')
#     connection, client_address = sock.accept()
#     print('connection from', client_address)
#     # Receive the data in small chunks and retransmit it
#     while True:
#         data = (connection.recv(1048))
#         #print(data)
#         #print('received {!r}'.format(data))
        
#         #print(JSON_string)
        
#         if data:
#             print(data)
#             print('sending data back to the client')
#             ack_packet = 'Data_recieved_by_raspberry_pi'
#             connection.sendall(ack_packet.encode("utf-8"))
#             print(data)
#             data = str(data)
#             JSON_string = data[(data.find('map_name')-2):(len(data))]
#             JSON_data = json.loads(data)
#             JSON_data = json.loads(JSON_string)
#             print(JSON_data)
#             print(JSON_data["map_name"])
#             temp_variable = JSON()
#             temp_variable.MAP_NAME              = str(JSON_data['map_name'])
#             temp_variable.MAP_CREATOR           = str(JSON_data['who_is_creating_the_map'])
#             temp_variable.GPS_LAT               = float(JSON_data['last_location']['latitude'])
#             temp_variable.GPS_LONG              = float(JSON_data['last_location']['longitude'])
#             temp_variable.calling_number        = str(JSON_data['calling_number'])
#             temp_variable.call_duration         = float(JSON_data['call_duration'])
#             temp_variable.TIME_BASED_TRIGGER    = (JSON_data['time_based_trigger'])
#             temp_variable.DISTANCE_BASED_TRIGGER= (JSON_data['distance_based_trigger'])
#             print(temp_variable)
#             pub_JSON.publish(temp_variable)
#             temp=0
#             print ("-----------------------------")

#         elif data == "Disconnect":
#             reply = "Disconnected and the listen has Stopped"
#             connection.send(reply.encode("utf-8"))
#             connection.close()
#             break
#         else:
#             reply = "Failed"
#             connection.send(reply.encode("utf-8"))
#             connection.close()
#             print ("-----------------------------")
#     connection.close()

