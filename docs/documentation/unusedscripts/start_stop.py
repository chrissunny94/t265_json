import rospy
import os
import rospy
import rospkg
import subprocess
import roslaunch
from std_srvs.srv import Trigger, TriggerResponse

def start_node_direct():
    """
    Does work as well from service/topic callbacks directly using rosrun
    """    
    package = 'YOUR_PACKAGE'
    node_name = 'YOUR_NODE.py'

    package = 'realsense2_camera'
    launch_file = 'rs_t265.launch'

    command = "roslaunch {0} {1}".format(package, launch_file)

    p = subprocess.Popen(command, shell=True)

    state = p.poll()
    if state is None:
        rospy.loginfo("process is running fine")
    elif state < 0:
        rospy.loginfo("Process terminated with error")
    elif state > 0:
        rospy.loginfo("Process terminated without error")


def start_node2():
    """
    Does work as well from service/topic callbacks using launch files
    """    
    package = 'realsense2_camera'
    launch_file = 'rs_t265.launch'

    command = "roslaunch  {0} {1}".format(package, launch_file)

    p = subprocess.Popen(command, shell=True)

    state = p.poll()
    if state is None:
        rospy.loginfo("process is running fine")
    elif state < 0:
        rospy.loginfo("Process terminated with error")
    elif state > 0:
        rospy.loginfo("Process terminated without error")

def start_node():
    """
    Does not work if called from service/topic callbacks due to main signaling issue
    """
    package = 'realsense2_camera'
    launch_file = 'rs_t265.launch'
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch_file = os.path.join(rospkg.RosPack().get_path(package), 'launch', launch_file)
    launch = roslaunch.parent.ROSLaunchParent(uuid, [launch_file])
    launch.start()
    #process = launch.launch(node)
    #print process.is_alive()
    #process.stop()

def service_callback(req):

    # edit below for other options
    #start_node()
    #start_node2()
    start_node_direct()

    return TriggerResponse(success=True)


def stop_callback(req):


    command = "rosnode kill /camera/realsense2_camera ;rosnode kill /camera/realsense2_camera_manage"

    p = subprocess.Popen(command, shell=True)

    state = p.poll()
    if state is None:
        rospy.loginfo("process is running fine")
    elif state < 0:
        rospy.loginfo("Process terminated with error")
    elif state > 0:
        rospy.loginfo("Process terminated without error")

    return TriggerResponse(success=True)

if __name__ == '__main__':
    rospy.init_node('test1', anonymous=True)

    service = rospy.Service('start_t265', Trigger, service_callback)

    service = rospy.Service('stop_t265', Trigger, stop_callback)

    rospy.spin()
