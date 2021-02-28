# t265_json




## Clone & install ros

```
mkdir ~/catkin_ws/src -p
cd ~/catkin_ws/src
git clone  https://github.com/chrissunny94/t265_json
cd t265_json
./install_ros_melodic_and_realsense_drivers_for_ubuntu.sh
```



## Build the workspace (build using catkin) 


```
cd ../../
catkin build
source devel/setup.bash
```


## How to use


```
roslaunch t265_json t265_node_without_rviz.launch

```



## Screenshots of a suitable APK

<img src="docs/android.jpeg" width="200">
<img src="docs/android1.jpeg" width="200">



