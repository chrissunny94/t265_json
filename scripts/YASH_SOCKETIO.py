#!/usr/bin/env python3
import socketio
import eventlet
import rospy, rospkg
from t265_json.msg import JSON
from std_msgs.msg import Int64 ,Bool
import json, os

os.system('fuser -$SIGNAL_NUMBER_OR_NAME -kn tcp 8081')
os.system('fuser -n tcp 8081')
global trigger_bool , mapping_status
trigger_bool= False
mapping_status = False





sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files = {
	'/': './public/'})


def trigger_callback( data):
	global mapping_status
	if (data.data and mapping_status):
		ack_packet = json.dumps( {"TRIGGER_CALL":True} ) 
		print(ack_packet)
		sio.emit(ack_packet.encode()) 
	global trigger_bool 
	trigger_bool= data.data


            

pub_JSON = rospy.Publisher('/JSON_from_phone', JSON, queue_size=1)  
pub_MAPPING_STATUS = rospy.Publisher('/MAPPING_STATUS', Bool, queue_size=1)
Trigger_sub = rospy.Subscriber('/android_call_trigger',Bool,trigger_callback)  

rospy.init_node('socket_server')
print("main")

def task(sid):
	#sio.sleep(5)
	result = sio.call('call_client', {'params': [3, 4]}, to= sid) 
	print("result: ", result)

@sio.event
def connect(sid, environ):
	print("Session Id: ", sid, "connected")	
	#sio.start_background_task(task, sid)


@sio.event
def disconnect(sid):
	print(sid, 'disconnected')

@sio.event
def stop_mapping(sid,data):
	print("stop mapping ")
	ack_packet = json.dumps({"stopped_mapping":True})
	print('\n\n\nsending data back to the client\n\n'+ack_packet)
	sio.emit(ack_packet.encode())
	pub_MAPPING_STATUS.publish(False)
	global mapping_status
	mapping_status = False


@sio.event
def start_mapping(sid, data):
	print(data)	
	JSON_data = json.loads(data)
	global trigger_bool ,mapping_status
	mapping_status = True
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
	ack_packet = json.dumps({"Data_recieved_by_raspberry_pi":True})
	sio.emit('my_response',ack_packet.encode())
	
            
	

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8081)), app)
