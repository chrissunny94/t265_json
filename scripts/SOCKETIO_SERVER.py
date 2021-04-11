#!/usr/bin/env python3
import eventlet
import socketio
import rospy, rospkg
from t265_json.msg import JSON
from std_msgs.msg import Int64 ,Bool
import json, os

global trigger_bool 
trigger_bool= False


def trigger_callback( data):
    if (data.data):
        ack_packet = json.dumps( {"TRIGGER_CALL":True} )  
    global trigger_bool 
    trigger_bool= data.data

            

pub_JSON = rospy.Publisher('/JSON_from_phone', JSON, queue_size=1)  
pub_MAPPING_STATUS = rospy.Publisher('/MAPPING_STATUS', Bool, queue_size=1)
Trigger_sub = rospy.Subscriber('/android_call_trigger',Bool,trigger_callback)  

rospy.init_node('socket_server')
print("main")


sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('message ', data)
    message = data.decode()
    print('Data received: {!r}'.format(message))
    JSON_data = json.loads(message)
    global trigger_bool

    if(trigger_bool):
        #self.client.settimeout(20)
        ack_packet = json.dumps( {"trigger_call":True} )
        print('\n\n\nsending data back to the client\n\n'+ack_packet)
        sio.emit(ack_packet.encode("utf-8"))
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
            sio.emit('my_response',ack_packet.encode())
                
            #print ("x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x")
            
        
        elif 'stop_mapping' in JSON_data:
            print("stop mapping ")
            ack_packet = json.dumps({"stopped_mapping":True})
            print('\n\n\nsending data back to the client\n\n'+ack_packet)
            sio.emit(ack_packet.encode())
            pub_MAPPING_STATUS.publish(False)
    

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.event
def send_data(sid, data):
    # handle the message
    return "OK", 123

HOST = str(os.popen('hostname -I').read())
#print(HOST)
IPV4HOST,sep,IPV6HOST = HOST.partition(' ')
print("\nIPV4Address:" +IPV4HOST + "\n")


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
