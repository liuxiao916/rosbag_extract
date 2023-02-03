import rosbag 	
import numpy as np
import cv2
import os
import argparse
from tqdm import * 
from cv_bridge import CvBridge 

parser = argparse.ArgumentParser()
parser.add_argument('--file_path', type=str, default='/media/xiao/NRSL12YEARS/forest.bag')
parser.add_argument('--topic', type=str, default='/depth/image_raw')
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
        if msg.encoding == "32FC1":
            cv_image = bridge.imgmsg_to_cv2(msg, "32FC1")
            image = np.array(cv_image, dtype=np.float)
            image=image*1000 # unit: m to mm
            NewImg = np.round(image).astype(np.uint16)
        elif msg.encoding == "16UC1":
            NewImg = bridge.imgmsg_to_cv2(msg, "16UC1")
        else:
            print("depth img format error")
            os._exit()

        if args.save_time:
            cv2.imwrite(os.path.join(args.save_dir, "{}.jpg".format(t)), NewImg)
        else:
            cv2.imwrite(os.path.join(args.save_dir, "{}.jpg".format(count)), NewImg)
        pbar.update()
        count +=1
        timestamp.append('{}'.format(t))