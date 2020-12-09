## What this script will do ?


This script will fetech the Odometry data from a ROS topic and publish it as a JSON file over  Socket communication .


## PRe requisites

```

sudo apt install python-catkin-tools
```



## Make a workspace , clone the repository and build



```

mkdir ~/REALSENSE_ws/src -p
cd ~/REALSENSE_ws/src
git clone https://github.com/chrissunny94/t265_json
cd ..
catkin build



```




## Install ROS and linux drivers for REALSENSE camera

*Once you are in the root of the cloned repository , please execute the following commands*

```
cd ~/REALSENSE_ws/src/t265_json

```

*Do the following to keep this repo upto date*

```
git pull
```


```
./install_realsense_on_raspberry.sh

./install_librealsense.sh
 
```









##  SOURCE THE REPOSITORY

```
cd ~/REALSENSE_ws
source devel/setup.bash
```




ALTERNATIVELY YOU CAN ADD THE ABOVE COMMAND TO ~/.bashrc

```
echo "source ~/REALSENSE_ws/devel/setup.bash" >> ~/.bashrc
```


## RUN THE T265 application

**THIS IS IF YOU HAVE THE PI CONNECTED TO A MONITOR **

```
roslaunch t265_json demo_t265.launch

```



## WITHOUT A MONITOR 

```
 roslaunch t265_json t265_node_without_rviz.launch
```



## Make the PI connect to a network

```
sudo pifi add <name-of-wifi-network> <password-of-wifi-network>
```































