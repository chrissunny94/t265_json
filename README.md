# t265_json

Requirement ,

UBUNTU LTS version either 14.04,16.04 ,18.04 , 20.04


Please install git 

```
sudo apt install git 
```


## Clone & install ros

```
mkdir ~/catkin_ws/src -p
cd ~/catkin_ws/src
git clone  https://github.com/chrissunny94/t265_json
cd t265_json
```





## Install the dependencies 


```
./install_ros_melodic_and_realsense_drivers_for_ubuntu.sh
```



## Build the workspace (build using catkin) 


```
cd ../../
catkin build
source devel/setup.bash
```


## How to use

The following will launch 3 things ,

- Real sense camera drivers

- Python script to interact with ANdroid APP

- Python script to interact with REALSENSE and ANdroid APP



```
cd ~/catkin_ws
source devel/setup.bash
roslaunch t265_json demo_t265.launch

```



## How to test without hardware 


```
roslaunch t265_json demo_t265_with_prerecordeddata.launch
```


## Screenshots of a suitable APK

<img src="docs/android.jpeg" width="200">
<img src="docs/android1.jpeg" width="200">



