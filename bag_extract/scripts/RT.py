#!/home/liuxiao/anaconda3/envs/ROS/bin/python
# RT.py
# Version 1.0


import rosbag 					       
import pandas as pd 
import numpy as np 
from tqdm import * 

filepath='/home/liuxiao/bagfiles/CA.bag'

bag = rosbag.Bag(filepath)
num=bag.get_message_count('/imu_raw')

time = []
x = []
y = []
z = []
w = []

#for topic, msg, t in bag.read_messages(topics=['/imu_']):
#	t.append(t)
#	x.append(msg.orientation.x)
#	y.append(msg.orientation.y)
#	z.append(msg.orientation.z)
#	w.append(msg.orientation.w)
#	data = np.array([t,x,y,z,w])
#	RT = pd.DataFrame(data.T, columns = ["t", "orientation.x", "orientation.y", "orientation.z","orientation.w"])

with tqdm(total=num) as pbar:
	count=0
	for topic, msg, t in bag.read_messages(topics=['/imu_raw']):
		time.append(t)
		x.append(msg.orientation.x)
		y.append(msg.orientation.y)
		z.append(msg.orientation.z)
		w.append(msg.orientation.w)
		pbar.update()
		count +=1


	data = np.array([time,x,y,z,w])
	RT = pd.DataFrame(data.T, columns = ["t", "orientation.x", "orientation.y", "orientation.z","orientation.w"])

bag.close()

RT.to_csv('/home/liuxiao/bagfiles/CA/IMU.csv')
