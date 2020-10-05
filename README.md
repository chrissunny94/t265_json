## What this script will do ?


This script will fetech the Odometry data from a ROS topic and publish it as a JSON file over  Socket communication .






## Pre Requisites .

Install ROS , 

* http://wiki.ros.org/ROS/Installation , for laptop/desktop , use this
* https://downloads.ubiquityrobotics.com/pi.html ,for raspberry Pi , use this .(*This comes preinstalled with ROS *)
	* Tested on 
	



## Instructions

* Run the python script for capturing ROS topic from T265 sensor and publishing the following contents in JSON
	   	
	
	
		python scripts/t265_ROS_topic_to_JSON.py		
  
   
    ![](docs/JSON_sample.jpg) 
    
   	* X/Latitude
   	* Y/Longitude
   	* Timestamp
   

* Run bag file 
		
		rosbag play bagfile/2020-09-25-17-29-33.bag -l


#### If you want  to run the server locally to echo out the JSON messages  and test , then  run the following
  
* Run http server for viewing JSON messages

		python3 scripts/server.py
	
		
  	
   		


### Additional Info 



[![IMAGE ALT TEXT](http://img.youtube.com/vi/o33gFBxLlyk/0.jpg)](http://www.youtube.com/watch?v=o33gFBxLlyk "Video Title")

We have attached a bagfile of what data the realsense sensor will put out when interfaced over ROS . 

If you type 

	$ rostopic list

Then you will see this .

	/camera/accel/imu_info
	/camera/accel/sample
	/camera/gyro/imu_info
	/camera/gyro/sample	
	/camera/odom/sample
	/camera/realsense2_camera_manager/bond
	/camera/tracking_module/parameter_descriptions
	/camera/tracking_module/parameter_updates
	/clock
	/diagnostics
	/rosout
	/rosout_agg
	/tf
	/tf_static



Of which , this is the topic of  our interest . This is what we are currently *fetching*  **from ROS** and *sending*  **out as JSON** .

	/camera/odom/sample
