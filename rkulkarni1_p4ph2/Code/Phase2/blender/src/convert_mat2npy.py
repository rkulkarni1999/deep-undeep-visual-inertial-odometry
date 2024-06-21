import numpy as np
from scipy.io import loadmat
import os

def convert_mat_to_npy(mat_filepath, npy_filepath):
    # Load the .mat file
    mat_data = loadmat(mat_filepath)
    
    time_array = mat_data['time']
    gyro_readings = mat_data['gyroReadings']
    accel_readings = mat_data['accelReadings'] 
    state_array = mat_data['state']
    
    loggedDict = {'time': time_array,
                  'state': state_array,
                  'gyro_readings' : gyro_readings,
                  'accel_readings' : accel_readings
                  }
    
    np.save(npy_filepath, loggedDict)

# Example usage
mat_filepath = './log/full_states_refactored_with_imu_circle_reverse.mat'  # Path to .mat file
npy_filepath = './log/full_states_refactored_with_imu_circle_reverse.npy'  # Desired path for the .npy file

convert_mat_to_npy(mat_filepath, npy_filepath)
print("Conversion complete. The .npy file has been saved to:", npy_filepath)
