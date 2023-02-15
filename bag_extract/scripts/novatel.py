#!/home/liuxiao/anaconda3/envs/ROS/bin/python
# RT.py
# Version 1.0


import rosbag 					       
import pandas as pd 
import numpy as np 
from tqdm import * 

filepath='/home/liuxiao/bagfiles/bancroft_clip.bag'

print('loading')
bag = rosbag.Bag(filepath)
num=bag.get_message_count('/novatel/oem7/inspva')

time = []
latitude = []
longitude = []
altitude = []
roll = []
pitch = []
azimuth = []





with tqdm(total=num) as pbar:
	count=0
	for topic, msg, t in bag.read_messages(topics=['/novatel/oem7/inspva']):
		time.append(t)
		latitude.append(msg.latitude)
		longitude.append(msg.longitude)
		altitude.append(msg.height)
		roll.append(msg.roll)
		pitch.append(msg.pitch)
		azimuth.append(msg.azimuth)

		pbar.update()
		count +=1


	data = np.array([time,latitude,longitude,altitude,roll,pitch,azimuth])
	RT = pd.DataFrame(data.T, columns = ["t", "latitude", "longtitude", "height","roll","pitch","azimuth"])

bag.close()

RT.to_csv('/home/liuxiao/bagfiles/bancroft_clip/novatel.csv')
