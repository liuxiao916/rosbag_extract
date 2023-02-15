from cv_bridge import CvBridge
import numpy as np
# create a 16bit depth image
im0 = np.empty(shape=(100, 100), dtype=np.uint16)
im0[:] = 2500 # 2.5m
print("original:", np.max(im0), im0.dtype)
# convert to compressed message
msg = CvBridge().cv2_to_compressed_imgmsg(im0, dst_format = "png")
# convert back to numpy array
im1 = CvBridge().compressed_imgmsg_to_cv2(msg)
print("converted:", np.max(im1), im1.dtype)
print("match?", np.all(im0==im1))