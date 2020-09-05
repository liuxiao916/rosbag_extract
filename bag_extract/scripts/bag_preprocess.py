#!/home/liuxiao/anaconda3/envs/ROS/bin/python
# bag_processing.py
# Version 1.0
""" Process images from rosbag into seperate folders in the current directory
	A lidar-camera synchronization file is also generated for refernce
	The current version supports only LIDAR and camera info. 

"""

import rosbag 
import os
import argparse
import cv2
from cv_bridge import CvBridge 
from sensor_msgs.msg import CompressedImage
import sys 
import time
from tqdm import *                                                             
from colorama import Fore, Back, Style 					       
import pandas as pd 
import numpy as np 

filepath='/home/liuxiao/bagfiles/bancroft_clip.bag'


def bag2image(topic_name,output_dir,num):
	with tqdm(total=num) as pbar:
		bridge = CvBridge()
		count=0
		timestamp=[]
		for topic, msg, t in bag.read_messages(topics=topic_name):
			#cv_img= bridge.imgmsg_to_cv2(msg,desired_encoding="passthrough")
			#cv2.imwrite(os.path.join(output_dir, "{}.jpg".format(t)), cv_img)
			#print 'Wrote image {}'.format(count)
			cv_img= bridge.compressed_imgmsg_to_cv2(msg,desired_encoding="passthrough")
			cv2.imwrite(os.path.join(output_dir, "{}.jpg".format(t)), cv_img)
			print 'Wrote image {}'.format(count)
			pbar.update()
			count +=1
			timestamp.append('{}'.format(t))
		return timestamp

print Fore.GREEN + 'Transformation starting... '
print Style.RESET_ALL

parents_path,filename=os.path.split(filepath)                                           
target_dir= '{}/{}'.format(parents_path,os.path.splitext(filename)[0])                 



if not os.path.isdir(target_dir):
	os.mkdir(target_dir)
	print 'New target folder created at {}'.format(target_dir)
else: 
	print 'Target folder existed. Continue... '




bag= rosbag.Bag(filepath)
num=bag.get_message_count('/rslidar_points')                                         #the parameter in bag.get_message_count() is topic name 



lidar_folder= '{}/lidar'.format(target_dir)


# YUNFAN HERE IS THE KEY PART!! 
if not os.path.isdir(lidar_folder):
	os.mkdir(lidar_folder)
print 'Transforming {} LIDAR point cloud files...'.format(num)
shell_command='rosrun pcl_ros bag_to_pcd {} /rslidar_points {} >/dev/null 2>&1'.format(filepath,lidar_folder)
os.system(shell_command)
print 'LIDAR DONE \n'


lidar_timestamp=[]
for root, dirs, files in os.walk(lidar_folder):                                    
	for file_name in files:
		temp= file_name.split('.')
		timestamp= temp[0] + temp[1]                                         
		lidar_timestamp.append(int(timestamp))
lidar_timestamp.sort()                                                             

lidar_list={'lidar':lidar_timestamp}                                                #a dictionary key = 'lidar' calue = lidar_timestamp
time_sync=pd.DataFrame(data=lidar_list)                                             



camera_list= ['cam0','cam1','cam2','cam3','cam4','cam5']        
for cam_name in camera_list:
	cam_folder= '{}/{}'.format(target_dir,cam_name) 
	if not os.path.isdir(cam_folder):
		os.mkdir(cam_folder)
	topic_name= '/camera_array/{}/image_raw/compressed'.format(cam_name)
	print '***Transforming Images for {}'.format(cam_name)
	cam_timestamp=bag2image(topic_name,cam_folder,num)                         
	print '{} DONE \n'.format(cam_name)
	sync_cam_time=[None]*num
	i=0
	for lidar_t in lidar_timestamp:
		if i<10:
			tmp=range(0,i+30)
		elif i> num-30:
			tmp = range(i-30,num)
		else:
			tmp= range(i-30, i+30)

		for q in tmp:

			if int(cam_timestamp[q])-lidar_t>0:
				sync_cam_time[i]=str(int(cam_timestamp[q]))
				#print '%19d' % sync_cam_time[i]
				break
		i+=1
	tmp_pd=pd.DataFrame({cam_name:list(sync_cam_time)})
	time_sync=time_sync.join(tmp_pd)
	print tmp_pd.head(10)
	print time_sync['cam0']
time_sync = time_sync.iloc[:num-8]
time_sync.to_csv('{}/{}_SYNC.csv'.format(target_dir,os.path.splitext(filename)[0]))



print Fore.GREEN + 'DONE transformation, SYNC file saved. '
print Style.RESET_ALL
