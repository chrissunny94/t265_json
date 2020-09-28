import json_transport
import rospy
from datetime import datetime

dateTimeObj = datetime.now()

rospy.init_node('json_talker')
pub = rospy.Publisher('json', json_transport.PackedJson, queue_size=1, latch=True)

pub.publish({'timestamp': 2, 'latitude': 1, 'longitude': 2})

msg = rospy.wait_for_message('json', json_transport.PackedJson)

assert msg.data == {'timestamp': 2, 'latitude': 1, 'longitude': 2}
