#!/usr/bin/env python3
import rospy, rospkg

import asyncio
from t265_json.msg import JSON
from std_msgs.msg import Int64 ,Bool
import os
import json

os.system('fuser -$SIGNAL_NUMBER_OR_NAME -kn tcp 8081')
os.system('fuser -n tcp 8081')

print("ROS PUBLISHERS")
global trigger_bool 
trigger_bool= False



pub_JSON = rospy.Publisher('/JSON_from_phone', JSON, queue_size=1)  
pub_MAPPING_STATUS = rospy.Publisher('/MAPPING_STATUS', Bool, queue_size=1)  

rospy.init_node('socket_server')
print("main")
            


class EchoServerClientProtocol(asyncio.Protocol):
    # def __init__(self):
        
    

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        #print('Connection from {}'.format(peername))
        self.transport = transport
        self.Trigger_sub = rospy.Subscriber('/android_call_trigger',Bool,self.trigger_callback)

    def trigger_callback(self ,data):
        if (data.data):
            ack_packet = json.dumps( {"TRIGGER_CALL":True} )  
            self.transport.write(ack_packet.encode())
        self.transport.close()  
        
    

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        JSON_data = json.loads(message)
        global trigger_bool

        if(trigger_bool):
            #self.client.settimeout(20)
            ack_packet = json.dumps( {"trigger_call":True} )
            print('\n\n\nsending data back to the client\n\n'+ack_packet)
            self.transport.write(ack_packet.encode("utf-8"))
            trigger_bool = False
        
        if ('BLANK' not in JSON_data):
            if 'map_name' in JSON_data:
                pub_MAPPING_STATUS.publish(True)
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
                pub_JSON.publish(temp_variable)
                ack_packet = json.dumbs({"Data_recieved_by_raspberry_pi":True})
                self.transport.write(ack_packet.encode())
                    
                #print ("x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x")
                
            
            elif 'stop_mapping' in JSON_data:
                print("stop mapping ")
                ack_packet = json.dumps({"stopped_mapping":True})
                print('\n\n\nsending data back to the client\n\n'+ack_packet)
                self.transport.write(ack_packet.encode())
                pub_MAPPING_STATUS.publish(False)
                    

        
        print('Close the client socket')
        self.transport.close()

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
HOST = str(os.popen('hostname -I').read())
print(HOST)
IPV4HOST,sep,IPV6HOST = HOST.partition(' ')
print(IPV4HOST)
coro = loop.create_server(EchoServerClientProtocol, IPV4HOST, 8081)
server = loop.run_until_complete(coro)

rate = rospy.Rate(1)


# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()