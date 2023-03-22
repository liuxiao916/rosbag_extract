import rosbag 	
import numpy as np
import os
import argparse
from tqdm import * 
import ros_numpy
import sensor_msgs


parser = argparse.ArgumentParser()
parser.add_argument('--file_path', type=str, default='/media/xiao/NRSL12YEARS1/2023-02-23-02-51-31.bag')
parser.add_argument('--topic', type=str, default='/ouster/points')
parser.add_argument('--save_dir', type=str, default='/media/xiao/NRSL12YEARS1/output/LiDAR_kitti')
args = parser.parse_args()

bag = rosbag.Bag(args.file_path)
num=bag.get_message_count(args.topic)

if not os.path.isdir(args.save_dir):
	os.mkdir(args.save_dir)
	print ('New target folder created at {}'.format(args.save_dir))
else: 
	print ('Target folder existed. Continue...' )

with tqdm(total=num) as pbar:
	count = 0
	timestamp = []
	for topic, msg, t in bag.read_messages(topics=args.topic):
		# Fix rosbag issues, see: https://github.com/eric-wieser/ros_numpy/issues/23
		msg.__class__ = sensor_msgs.msg._PointCloud2.PointCloud2
		offset_sorted = {f.offset: f for f in msg.fields}
		msg.fields = [f for (_, f) in sorted(offset_sorted.items())]

		#points_np_struct = ros_numpy.point_cloud2.pointcloud2_to_array(msg)
		points_np_struct = ros_numpy.numpify(msg).reshape(-1)
		#Img: (64,1024). The channels are x, y ,z, intensity, t, reflectivity, ring, ambient, and range
		points_np = np.zeros((points_np_struct.shape[0], 4), dtype=np.float32)
		points_np[:, 0] = points_np_struct['x']
		points_np[:, 1] = points_np_struct['y']
		points_np[:, 2] = points_np_struct['z']
		try:
			points_np[:, 3] = points_np_struct['intensity']
		except:
			pass
		file_name = args.save_dir + '/%s.bin' % (str(count).zfill(6))
		with open(file_name, 'w') as f:
			points_np.tofile(f)

		pbar.update()
		count += 1
		timestamp.append('{}'.format(t))
