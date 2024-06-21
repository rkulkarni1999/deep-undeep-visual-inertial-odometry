# import numpy as np
# import math
# # Specify the path to your .npy file
# npy_file_path = '/home/pear_group/rutwik/P4/DeepIO/KITTI/pose_GT/raw_data/final_data_absolute_relative_square_kids_rug_io.npy'

# # Load the array from the .npy file
# all_data = (np.load(npy_file_path,allow_pickle=True).item())['data_absolute']


# def quaternion_to_rpy(quaternions):
#     # Assume quaternions is an Nx4 matrix where each row is [qw, qx, qy, qz]
#     qw = quaternions[:, 0]
#     qx = quaternions[:, 1]
#     qy = quaternions[:, 2]
#     qz = quaternions[:, 3]

#     # Calculate the roll (x-axis rotation)
#     sinr_cosp = 2 * (qw * qx + qy * qz)
#     cosr_cosp = 1 - 2 * (qx**2 + qy**2)
#     roll = np.arctan2(sinr_cosp, cosr_cosp)

#     # Calculate the pitch (y-axis rotation)
#     sinp = 2 * (qw * qy - qz * qx)
#     pitch = np.where(np.abs(sinp) >= 1,
#                      np.copysign(np.pi / 2, sinp),
#                      np.arcsin(sinp))

#     # Calculate the yaw (z-axis rotation)
#     siny_cosp = 2 * (qw * qz + qx * qy)
#     cosy_cosp = 1 - 2 * (qy**2 + qz**2)
#     yaw = np.arctan2(siny_cosp, cosy_cosp)

#     # Convert angles from radians to degrees
#     roll = np.degrees(roll)
#     pitch = np.degrees(pitch)
#     yaw = np.degrees(yaw)
#     return np.column_stack((roll, pitch, yaw))


# def quaternions_to_rotation_matrices_flat(quaternions):
#     # Normalizing the quaternion rows
#     norms = np.linalg.norm(quaternions, axis=1, keepdims=True)
#     quaternions = quaternions / norms

#     # Extracting individual components
#     qw = quaternions[:, 0]
#     qx = quaternions[:, 1]
#     qy = quaternions[:, 2]
#     qz = quaternions[:, 3]

#     # Pre-computing repeated values
#     qx2 = qx * qx
#     qy2 = qy * qy
#     qz2 = qz * qz
#     qxqy = qx * qy
#     qxqz = qx * qz
#     qyqz = qy * qz
#     qxqw = qx * qw
#     qyqw = qy * qw
#     qzqw = qz * qw

#     # Assembling the rotation matrix for each quaternion
#     R = np.zeros((len(quaternions), 9))
#     R[:, 0] = 1 - 2 * (qy2 + qz2)
#     R[:, 1] = 2 * (qxqy - qzqw)
#     R[:, 2] = 2 * (qxqz + qyqw)
#     R[:, 3] = 2 * (qxqy + qzqw)
#     R[:, 4] = 1 - 2 * (qx2 + qz2)
#     R[:, 5] = 2 * (qyqz - qxqw)
#     R[:, 6] = 2 * (qxqz - qyqw)
#     R[:, 7] = 2 * (qyqz + qxqw)
#     R[:, 8] = 1 - 2 * (qx2 + qy2)

#     return R
# # Print the loaded data to verify it has been read correctly
# # data = np.zeros((int(all_data.shape[0]/10),17))
# # count = 0
# # for i in range(0,all_data.shape[0]-2,10):
# #     data[count,:] = all_data[i,:]
# #     count +=1

# # print(data.shape)
# data = all_data
# theta = quaternion_to_rpy(data[:,7:11])
# print("EULER",theta.shape)
# R = quaternions_to_rotation_matrices_flat(data[:,7:11])
# print("rotation",R.shape)
# T = data[:,1:4]
# print("position", T.shape)
# IMU = data[:,11:17]
# pose = np.concatenate((theta,T,R,IMU), axis=1)
# filename = '/home/pear_group/rutwik/P4/DeepIO/KITTI/pose_GT/06.npy'

# # Save the matrix to a .npy file
# print(pose.shape)
# np.save(filename, pose)


import pickle
import pandas as pd


# Path to the pickle file
pickle_file_path = '/home/pear_group/rutwik/P4/DeepIO/datainfo/train_df_t010203040506_v04_pNone_seq5x5_sample3.pickle'

# Open the pickle file and load the data
with open(pickle_file_path, 'rb') as file:
    data = pd.read_pickle(file)

# Now you can use the data
print(data)