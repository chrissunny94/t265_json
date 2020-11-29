## What this script will do ?


This script will fetech the Odometry data from a ROS topic and publish it as a JSON file over  Socket communication .



## Make a workspace , clone the repository and build



```

mkdir ~/REALSENSE_ws/src -p
cd ~/REALSENSE_ws/src
git clone https://github.com/chrissunny94/t265_json
cd ..
catkin_make

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


```
roslaunch t265_json demo_t265.launch

```
































