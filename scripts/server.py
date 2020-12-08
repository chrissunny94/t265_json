#!/usr/bin/env python3
import socket
import threading
import os 
from t265_json.msg import JSON
import rospy
import json


os.system('fuser -$SIGNAL_NUMBER_OR_NAME -kn tcp 8081')

#Variables for holding information about connections
connections = []
total_connections = 0







#Client class, new instance created for each connected client
#Each instance has the socket and address that is associated with items
#Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
        self.pub_JSON = rospy.Publisher('/JSON_from_phone', JSON, queue_size=10)
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    #Attempt to get data from client
    #If unable to, assume client has disconnected and remove him from server data
    #If able to and we get data back, print it in the server and send it back to every
    #client aside from the client that has sent it
    #.decode is used to convert the byte data into a printable string
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(64)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                #@Sharath you have to stuff this with data extracted from JSON
                JSON_string = data[(data.find('map_name')-2):(len(data)-1)]
                print(JSON_string)
                JSON_data = json.loads(JSON_string)
                temp_variable = JSON()
                temp_variable.MAP_NAME=JSON_data['map_name']
                temp_variable.MAP_CREATOR=JSON_data['who_is_creating_the_map']
                temp_variable.GPS_LAT=JSON_data['last_location']['latitude']
                temp_variable.GPS_LONG=JSON_data['last_location']['longitude']
                temp_variable.calling_number=JSON_data['calling_number']
                temp_variable.call_duration=JSON_data['call_duration']
                temp_variable.TIME_BASED_TRIGGER=JSON_data['time_based_trigger']
                temp_variable.DISTANCE_BASED_TRIGGER=JSON_data['distance_based_trigger']
                print(temp_variable)
                self.pub_JSON.publish(temp_variable)
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)
    def join(self):
        return 1

#Wait for new connections
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1

def main():
    
    rospy.init_node('JSON_server_simple', anonymous=True)
    
    hostname = socket.gethostname()
    print("Your Computer Name is:" + hostname)    
    host = str(os.popen('hostname -I').read())
    host = host.replace("\n","")
    host = host.replace(' ','')
    print("Your Computer IP Address is:" + host)  
    port = 8081
    print("Port:",port)
    #Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    #Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()
    
main()
