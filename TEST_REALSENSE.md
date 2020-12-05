# Document to test the working of the realsense camera


## command to see if the drivers are installed and it works .

```
rs-enumerate-devices
```


## GUI provided by  intel 

```
realsense-viewer
```


## ROS tests

```
roslanch realsense2_camera rs_t265.launch
```



This would launch the ROS drivers for realsense camera 

You can then perform 

```
rostopic list

rostopic hz /camera/odom/sample

rostopic echo /camera/odom/sample

```
