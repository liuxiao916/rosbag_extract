# rosbag_extract
These are some scripts to extract data from rosbag conveniently. Any contribution is welcome.

## Install 
``` bash
sudo apt install python3-rosbag 
sudo apt-get install ros-noetic-ros-numpy
pip3 install tqdm opencv-python argparse cv-bridge
```

## Get_image
This script is used to extract image data from rosbag. It supports `sensor_msgs/Image` and `sensor_msgs/CompressedImage`. Please modify script file before run it. You should specify your bag file path, output directory, topic name ,sensor_msgs type,and whether save with timestamp.  

```bash
./scripts/get_image.sh
```

## Get_depth_image
This is used to extract depth image data. 

## Get_LiDAR
This is used to extract LiDAR data as .pcd files with pcl_ros. 

## Get_LiDAR_kitti
Extract LiDAR data and save in kitti format. (000000.bin). Tests on Ouster LiDAR.

## Template 
You can extract other kinds of data by editing Template.py

## Old package 
bag_preprocess.py is used to get photos and lidar data from rosbag


