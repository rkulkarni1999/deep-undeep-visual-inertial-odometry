import numpy as np
import scipy
import math


def compute_euler_rates(delta_euler_angles, time_array):
    euler_rates = []

    for i in range(1, len(time_array)):
        delta_time = time_array[i] - time_array[i - 1]
        rate = delta_euler_angles[i - 1] / delta_time
        euler_rates.append(rate)

    return np.array(euler_rates)

def rotation_matrix_to_euler_angles(R):
    psi = np.arctan2(R[1, 0], R[0, 0])
    theta = np.arcsin(-R[2, 0])
    phi = np.arctan2(R[2, 1], R[2, 2])
    
    roll = phi
    pitch = theta
    yaw = psi

    return roll, pitch, yaw

def calculate_delta_euler_angles(rotation_matrices):
    
    delta_euler_angles = []
    for i in range(1, len(rotation_matrices)):
        # Calculate delta rotation matrix from previous to current
        delta_rotation_matrix = np.linalg.inv(rotation_matrices[i-1]) @ rotation_matrices[i]
        # Calculate euler angles for this delta rotation
        delta_euler = rotation_matrix_to_euler_angles(delta_rotation_matrix)
        delta_euler_angles.append(delta_euler)
    
    return np.array(delta_euler_angles)

def compute_relative_accelerations(accelerations, rotation_matrices):
    # Initialize a list to store transformed accelerations, starting with the first one unchanged
    # because there's no "previous" rotation matrix for the first frame
    transformed_accelerations = [accelerations[0]]  # Assuming the first acceleration is aligned with the first frame

    # Transform each subsequent acceleration using the rotation matrix of the previous frame
    for i in range(1, len(accelerations)):
        previous_R = rotation_matrices[i - 1]
        transformed_accelerations.append(np.linalg.inv(previous_R) @ accelerations[i])

    return np.array(transformed_accelerations)

def compute_relative_angular_vels(angular_velocities, rotation_matrices):
    # Initialize a list to store transformed accelerations, starting with the first one unchanged
    # because there's no "previous" rotation matrix for the first frame
    transformed_angVels = []  # Assuming the first acceleration is aligned with the first frame

    # Transform each subsequent acceleration using the rotation matrix of the previous frame
    for i in range(0, len(angular_velocities)):
        previous_R = rotation_matrices[i]
        transformed_angVels.append(previous_R.T @ angular_velocities[i])

    return np.array(transformed_angVels)

def load_logged_data():
    # Loads the data from the .npy file
    data = np.load('./log/states_circle.npy', allow_pickle=True).item()
    return data

# quaternion to rotation
def quaternion_to_rotation_matrix(q):
    """ Convert a quaternion to a rotation matrix. """
    qw, qx, qy, qz = q
    R = np.array([
        [1 - 2*qy**2 - 2*qz**2, 2*qx*qy - 2*qz*qw, 2*qx*qz + 2*qy*qw],
        [2*qx*qy + 2*qz*qw, 1 - 2*qx**2 - 2*qz**2, 2*qy*qz - 2*qx*qw],
        [2*qx*qz - 2*qy*qw, 2*qy*qz + 2*qx*qw, 1 - 2*qx**2 - 2*qy**2]
    ])
    return R

def quaternion_to_rpy(qw, qx, qy, qz):
    # Convert quaternion to roll, pitch, yaw
    sinr_cosp = 2 * (qw * qx + qy * qz)
    cosr_cosp = 1 - 2 * (qx * qx + qy * qy)
    roll = math.atan2(sinr_cosp, cosr_cosp)
    
    sinp = 2 * (qw * qy - qz * qx)
    pitch = math.asin(sinp) if abs(sinp) < 1 else math.copysign(math.pi / 2, sinp)
    
    siny_cosp = 2 * (qw * qz + qx * qy)
    cosy_cosp = 1 - 2 * (qy * qy + qz * qz)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return np.degrees(roll), np.degrees(pitch), np.degrees(yaw)

def euler_to_rotation_matrix(roll, pitch, yaw):
    # Convert Euler angles (degrees) to a rotation matrix
    roll, pitch, yaw = np.radians([roll, pitch, yaw])
    Rx = np.array([
        [1, 0, 0],
        [0, math.cos(roll), -math.sin(roll)],
        [0, math.sin(roll), math.cos(roll)]
    ])
    Ry = np.array([
        [math.cos(pitch), 0, math.sin(pitch)],
        [0, 1, 0],
        [-math.sin(pitch), 0, math.cos(pitch)]
    ])
    Rz = np.array([
        [math.cos(yaw), -math.sin(yaw), 0],
        [math.sin(yaw), math.cos(yaw), 0],
        [0, 0, 1]
    ])
    R = Rz @ Ry @ Rx
    return R

if __name__ == "__main__":

    # loading the data
    logged_data = load_logged_data()
    
    # timestamps 
    time_array = logged_data['time']
    
    # state_array : position, linear vel, orientation in quat, angular vel, linear accelerations
    state_array = logged_data['state']
    
    # state derivative array : derivative(state_array)
    state_derivative_array = logged_data['state_derivative']
    
    # # Downsample IMU Readings
    # time_array = time_array[::10]
    # state_array = state_array[::10]
    # state_derivative_array = state_derivative_array[::10]

    # extract acceletation = derivative(linear_vel)
    acceleration = state_derivative_array[:, 3:6]
    
    # extract quaternion from state array
    orientation_quaternions = state_array[:, 6:10]

    # extract angular velocities
    angular_velocities = state_array[:, 10:13]

    # compute rotation matrix from quaternion
    rotation_matrices = np.array([quaternion_to_rotation_matrix(q) for q in orientation_quaternions])
    
    # compute relative angular rates
    relative_angular_velocities = compute_relative_angular_vels(angular_velocities, rotation_matrices)
    state_array[:, 10:13] = relative_angular_velocities

    # compute relative accelerations 
    relative_accelerations = compute_relative_accelerations(acceleration, rotation_matrices)
    
    # store acceleration data in the data araray. 
    full_state = np.hstack((state_array, relative_accelerations))
    
    # # Drop last 
    # full_state = full_state[:len(full_state)-1,:] # dropping the last state for compliance with images
    # time_array = time_array[:len(time_array)-1]

    # Drop last 2 
    full_state = full_state[:len(full_state)-2,:] # dropping the last state for compliance with images
    time_array = time_array[:len(time_array)-2]

    # changing the logged data format
    loggedDict = {'time': time_array,                       # timestamps
                  'state': full_state,                      # position, vel, orientation wrt world frame, ang_vel and acc wrt body
                  'rotation_matrices': rotation_matrices}   # Orientations in the form of rotation matrices in world frame. 
    
    # saving in a .mat file for matlab. 
    scipy.io.savemat('./log/full_states_for_imuSensor_circle.mat', loggedDict)
    np.save('./log/full_states_for_imuSensor_circle.npy', loggedDict)

    



    
    