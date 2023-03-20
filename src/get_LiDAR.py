import rosbag 	
import numpy as np
import os
import argparse
from tqdm import * 


parser = argparse.ArgumentParser()
parser.add_argument('--file_path', type=str, default='/media/xiao/NRSL12YEARS1/2023-02-23-02-51-31.bag')
parser.add_argument('--topic', type=str, default='/ouster/points')
parser.add_argument('--save_dir', type=str, default='/media/xiao/NRSL12YEARS1/output/LiDAR')
args = parser.parse_args()

bag = rosbag.Bag(args.file_path)
num=bag.get_message_count(args.topic)

if not os.path.isdir(args.save_dir):
	os.mkdir(args.save_dir)
	print ('New target folder created at {}'.format(args.save_dir))
else: 
	print ('Target folder existed. Continue...' )

print('Transforming {} LIDAR point cloud files...'.format(num))
shell_command = 'rosrun pcl_ros bag_to_pcd {} {} {} >/dev/null 2>&1'.format(args.file_path, args.topic, args.save_dir)
os.system(shell_command)
print('Done')