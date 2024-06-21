import os
from torchvision import transforms
from PIL import Image
import torch
import math
import numpy as np

def rename_images(directory, new_name_base):
    """
    Renames all image files in the specified directory to a new name with an index.

    Args:
    directory (str): The path to the directory containing the images.
    new_name_base (str): Base name for the new file names.
    """
    # Get a list of all files in the directory
    files = os.listdir(directory)

    # Filter out files to only include images (you can add more extensions as needed)
    image_files = [f for f in files if f.lower().endswith(('.jpg'))]

    # Sort files to maintain any existing order
    image_files.sort()

    # Rename each image file
    for index, filename in enumerate(image_files, start=1):
        # Create the new file name with an index
        extension = os.path.splitext(filename)[1]  # Gets the file extension
        new_name = f"{new_name_base}{index:0{4}d}{extension}"
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)

        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed '{filename}' to '{new_name}'")


def calculate_rgb_mean_std(directory, minus_point_5=False):
	
    files = os.listdir(directory)

    # Filter out files to only include images (you can add more extensions as needed)
    image_files = [f for f in files if f.lower().endswith(('.jpg'))]

    # Sort files to maintain any existing order
    image_files.sort()

    n_images = len(image_files)
    cnt_pixels = 0
    print('Numbers of frames in training dataset: {}'.format(n_images))
    mean_np = [0, 0, 0]
    mean_tensor = [0, 0, 0]
    to_tensor = transforms.ToTensor()

    image_sequence = []
    for idx, img_name in enumerate(image_files):
        print('{} / {}'.format(idx, n_images), end='\r')
        img_path = os.path.join('/home/ankit/Documents/STUDY1/RBE594/p4ph2/DeepVO-pytorch/KITTI/images/00',img_name)
        img_as_img = Image.open(img_path)
        img_as_tensor = to_tensor(img_as_img)
        if minus_point_5:
            img_as_tensor = img_as_tensor - 0.5
        img_as_np = np.array(img_as_img)
        img_as_np = np.rollaxis(img_as_np, 2, 0)
        cnt_pixels += img_as_np.shape[1]*img_as_np.shape[2]
        for c in range(3):
            mean_tensor[c] += float(torch.sum(img_as_tensor[c]))
            mean_np[c] += float(np.sum(img_as_np[c]))
    mean_tensor =  [v / cnt_pixels for v in mean_tensor]
    mean_np = [v / cnt_pixels for v in mean_np]
    print('mean_tensor = ', mean_tensor)
    print('mean_np = ', mean_np)

    std_tensor = [0, 0, 0]
    std_np = [0, 0, 0]
    for idx, img_name in enumerate(image_files):
        print('{} / {}'.format(idx, n_images), end='\r')
        img_path = os.path.join('/home/ankit/Documents/STUDY1/RBE594/p4ph2/DeepVO-pytorch/KITTI/images/00',img_name)
        img_as_img = Image.open(img_path)
        img_as_tensor = to_tensor(img_as_img)
        if minus_point_5:
            img_as_tensor = img_as_tensor - 0.5
        img_as_np = np.array(img_as_img)
        img_as_np = np.rollaxis(img_as_np, 2, 0)
        for c in range(3):
            tmp = (img_as_tensor[c] - mean_tensor[c])**2
            std_tensor[c] += float(torch.sum(tmp))
            tmp = (img_as_np[c] - mean_np[c])**2
            std_np[c] += float(np.sum(tmp))
    std_tensor = [math.sqrt(v / cnt_pixels) for v in std_tensor]
    std_np = [math.sqrt(v / cnt_pixels) for v in std_np]
    print('std_tensor = ', std_tensor)
    print('std_np = ', std_np)

# Usage example
directory_path = '/home/ankit/Documents/STUDY1/RBE594/p4ph2/DeepVO-pytorch/KITTI/images/00'
# rename_images(directory_path, 'image')
calculate_rgb_mean_std(directory_path)