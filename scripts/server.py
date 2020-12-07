#!/usr/bin/env python3
import socket
import threading
import os 
from t265_json.msg import JSON
import rospy


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
        self.pub_JSON = rospy.Publisher('JSON_from_phone', JSON, queue_size=10)
    
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
                temp_variable = JSON()
                temp_variable.MAP_NAME
                temp_variable.MAP_CREATOR
                temp_variable.GPS_LAT
                temp_variable.GPS_LONG
                temp_variable.calling_number
                temp_variable.call_duration
                temp_variable.TIME_BASED_TRIGGER
                temp_variable.DISTANCE_BASED_TRIGGER
                self.pub_JSON(temp_variable)
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)

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
    #Get host and port
    #host = input("Host: ")
    hostname = socket.gethostname()
    host=socket.gethostbyname(hostname)
    #print([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]  if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
    
    #print ("IP Address =",l)
    #host = l[0]
    host = str(os.system('hostname -I'))
    print("Your Computer Name is:" + hostname)    
    print("Your Computer IP Address is:" + host)  
    #port = int(input("Port: "))
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
