import rclpy
from rclpy.node import Node
import rosbag2_py
from rclpy.serialization import deserialize_message
import argparse
from tqdm import * 
from cv_bridge import CvBridge 
from sensor_msgs.msg import Image
import cv2
import os

class BagReader(Node):
    def __init__(self, args):
        super().__init__('bag_reader')
        self.bag_path = args.file_path
        self.topic_name = args.topic
        self.compressed_img = args.compressed_img
        self.save_time = args.save_time
        self.save_dir = args.save_dir

        self.read_bag()

    def read_bag(self):
        if not os.path.isdir(self.save_dir):
            os.mkdir(self.save_dir)
            print ('New target folder created at {}'.format(self.save_dir))
        else: 
            print ('Target folder existed. Continue...' )


        storage_options = rosbag2_py.StorageOptions(uri=self.bag_path, storage_id='sqlite3')
        converter_options = rosbag2_py.ConverterOptions()
        reader = rosbag2_py.SequentialReader()
        reader.open(storage_options, converter_options)

        topic_types = reader.get_all_topics_and_types()
        type_map = {t.name: t.type for t in topic_types}
        metadata = reader.get_metadata()
        count_map = {t.topic_metadata.name: t.message_count for t in metadata.topics_with_message_count}
        if self.topic_name not in type_map:
            self.get_logger().error(f"Topic {self.topic_name} not found in bag file.")
            return
        
        msg_count = count_map[self.topic_name]

        reader.seek(0) 
        with tqdm(total=msg_count) as pbar:
            bridge = CvBridge()
            count=0
            timestamp=[]
            while reader.has_next():
                topic, msg_data, t = reader.read_next()
                if topic == self.topic_name:
                    msg = deserialize_message(msg_data, Image)
                    if self.compressed_img:
                        cv_img= bridge.compressed_imgmsg_to_cv2(msg,desired_encoding="passthrough")
                    else:
                        cv_img= bridge.imgmsg_to_cv2(msg,desired_encoding="passthrough")
                    cv_img = cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)

                    if self.save_time:
                        cv2.imwrite(os.path.join(self.save_dir, "{}.jpg".format(t)), cv_img)
                    else:
                        cv2.imwrite(os.path.join(self.save_dir, "{}.jpg".format(count)), cv_img)
                    pbar.update()
                    count +=1
                    timestamp.append('{}'.format(t))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, default='/media/nros-xiao-2404/HDD1/bag2/rosbag2_2025_02_18-15_16_12')
    parser.add_argument('--topic', type=str, default='/d435_throttle')
    parser.add_argument('--save_dir', type=str, default='/media/nros-xiao-2404/HDD1/bag2/output/img')
    parser.add_argument('--compressed_img', type=bool, default=False)
    parser.add_argument('--save_time', type=bool, default=True)
    args = parser.parse_args()

    rclpy.init()
    node = BagReader(args)
    rclpy.shutdown()

if __name__ == '__main__':
    main()