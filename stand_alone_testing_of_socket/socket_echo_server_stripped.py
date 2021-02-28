#!/usr/bin/env python3
import csv
import os
import math
import socket
import json
from datetime import datetime
import sys , os

os.system('fuser -$SIGNAL_NUMBER_OR_NAME -kn tcp 8081')
os.system('fuser -n tcp 8081')



class T265JsonServer():

    def __init__(self):
        print("Class constructor")
        self.trigger_bool = False
        self.current_time = 0
        hostname = socket.gethostname()
        print("Your Computer Name is:" + hostname)    
        HOST = str(os.popen('hostname -I').read())
        HOST = HOST.replace("\n","")
        HOST = HOST.replace(" ","")
        self.HOST = HOST
        PORT = 8081         # The port used by the server
        self.PORT = PORT
        print("Setting IP address:",self.HOST)
        print("Setting PORT:",self.PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        print("T265 JSON CLASS INITIATED")
        self.socket_loop_function()
    

    def socket_loop_function(self):
        try:
            print("\nSocket")
            self.client.bind((self.HOST, self.PORT))
            self.client.listen(10) # how many connections can it receive at one time
            print ("Start Listening...")
            while True:
                try:
                    #self.client.settimeout(3)
                    conn, addr = self.client.accept()
                    print ("client with address: ", addr, " is connected.")
                    #conn.settimeout(5)
                    #conn.setblocking(0)
                    data = conn.recv(1024)
                    JSON_data = json.loads(data)
                    # print ("Recieved this data: <", JSON_data, "> from the client.")
                except :
                    JSON_data = {"BLANK":True}
                    conn = False

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
                            print('\nsending data back to the client')
                            ack_packet = json.dumps({"Data_recieved_by_raspberry_pi":True})
                            conn.sendall(ack_packet.encode("utf-8"))
                            print(ack_packet)
                            print(JSON_data["map_name"])
                            print ("x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x")
                        
                        elif 'stop_mapping' in JSON_data:
                            print("stop mapping ")
                            ack_packet = json.dumps({"stopped_mapping":True})
                            print('\n\n\nsending data back to the client\n\n'+ack_packet)
                            conn.sendall(ack_packet.encode("utf-8"))
                    else:
                        print('\nNODATA')
                elif(not conn):
                    print("\nNo connection")
                    if(self.trigger_bool):
                        print("No socket connection")
            pass
        except KeyboardInterrupt:
            pass
    


    
if __name__ == '__main__':
    
    print("main")
    T265JsonServer()
        
    





