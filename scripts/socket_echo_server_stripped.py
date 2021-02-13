#/usr/bin/env python3
import socket
import sys , os
import json
import sys


os.system('fuser -$SIGNAL_NUMBER_OR_NAME -kn tcp 8081')
os.system('fuser -n tcp 8081')

# Create a TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port


HOST = str(os.popen('hostname -I').read())
HOST = HOST.replace("\n","")
HOST = HOST.replace(" ","")
print("Your Computer IP Address is:",HOST)  

PORT = 8081
print("Port:",PORT)


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
        #print ("Recieved this data: <", data, "> from the client.")
        JSON_data = json.loads(data)

        if 'map_name' in JSON_data:
            ack_packet = 'Data_recieved_by_raspberry_pi'
            print('\n\n\nsending data back to the client\n\n'+ack_packet)
            conn.sendall(ack_packet.encode("utf-8"))
            #print(data)
            JSON_data = json.loads(data)
            print(JSON_data)
            # print(str(JSON_data['map_name']))
            # print(str(JSON_data['map_created_by'] ))
            # print(float(JSON_data['last_location']['system_latitude']))
            # print(float(JSON_data['last_location']['system_longitude']))
            # print(str(JSON_data['calling_number']))
            # print(float(JSON_data['call_duration']))
            # try:
            #     print( (JSON_data['trigger_time_based']))
            # except :
            #     pass
            
            # try:
            #     print(JSON_data['trigger_distance_based'])
            # except :
            #     pass
            # print ("\n\nx-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x\n\n")

        
            print("start mapping ")
            ack_packet = json.dumps({"started_mapping":True})
            print('\n\n\nsending data back to the client\n\n'+ack_packet)
            conn.sendall(ack_packet.encode("utf-8"))
        elif 'stop_mapping' in JSON_data:
            print("stop mapping ")
            ack_packet = json.dumps({"stopped_mapping":True})
            print('\n\n\nsending data back to the client\n\n'+ack_packet)
            conn.sendall(ack_packet.encode("utf-8"))


        elif data == "Correct":
            reply = "Success"
            conn.send(reply.encode("utf-8"))
            conn.close()
            print ("\n-----------------------------\n")
        elif data == "Disconnect":
            reply = "Disconnected and the listen has Stopped"
            conn.send(reply.encode("utf-8"))
            conn.close()
            break
        else:
            reply = "Failed"
            conn.send(reply.encode("utf-8"))
            conn.close()
            print ("\n-----------------------------\n")
            
    client.close()
"""
You can use thread for the recieve operation so that the execution in main thread
isn't wait until complete the recieve operation. 
"""
#thread = threading.Thread(target = recvFromAndroid, args = ())
#thread.start()
recv()
print( "completed")


