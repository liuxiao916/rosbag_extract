# rosbag_extract
These are some scripts to extract data from rosbag conveniently. Any contribution is welcome.

## Install 
``` bash
sudo apt install python3-rosbag
pip3 install tqdm
pip3 install opencv-python
pip3 install argparse
pip3 install cv-bridge
```

## Get_image
This script is used to extract image data from rosbag. It support `sensor_msgs/Image` and `sensor_msgs/CompressedImage`. Please modify script file before run it. You should specify your bag file path, output directory, topic name ,sensor_msgs type,and whether save with timestamp.  

```bash
./scripts/get_image.sh
```

## Old package 
bag_preprocess.py is used to get photos and lidar data from rosbag


