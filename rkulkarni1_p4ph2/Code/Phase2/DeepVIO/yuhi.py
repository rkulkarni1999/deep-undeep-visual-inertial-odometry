
import glob
import os
from PIL import Image
import numpy as np
# image_dir = "/home/ankit/Documents/STUDY1/RBE594/p4ph2/DeepVO-pytorch/KITTI/images/"
# folder = '00'
# path = os.path.join(image_dir,folder,'*.jpg')
# path1 ="/home/ankit/Documents/STUDY1/RBE594/p4ph2/DeepVO-pytorch/KITTI/images/00"
# fpaths = glob.glob(path)
# print(len(fpaths))
img_path = "/home/ankit/Documents/STUDY1/RBE594/p4ph2/DeepVIO/KITTI/images/00/image0001.jpg"
img_as_img = Image.open(img_path)
print(np.array(img_as_img))