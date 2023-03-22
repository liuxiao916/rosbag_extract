import rosbag 	
import cv2
import os
import argparse
from tqdm import * 
from cv_bridge import CvBridge 

parser = argparse.ArgumentParser()
parser.add_argument('--file_path', type=str, default='/media/xiao/NRSL12YEARS/forest.bag')
parser.add_argument('--topic', type=str, default='/image_raw')
parser.add_argument('--save_dir', type=str, default='/media/xiao/NRSL12YEARS/output/img')
parser.add_argument('--save_time', type=bool, default=False)
args = parser.parse_args()

bag = rosbag.Bag(args.file_path)
num=bag.get_message_count(args.topic)

if not os.path.isdir(args.save_dir):
	os.mkdir(args.save_dir)
	print ('New target folder created at {}'.format(args.save_dir))
else: 
	print ('Target folder existed. Continue...' )

with tqdm(total=num) as pbar:
    bridge = CvBridge()
    count=0
    timestamp=[]
    for topic, msg, t in bag.read_messages(topics=args.topic):
        # Write code to save msg

        pbar.update()
        count +=1
        timestamp.append('{}'.format(t))