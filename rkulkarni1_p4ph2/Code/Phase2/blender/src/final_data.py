import numpy as np
import scipy


# # Indices for Data Absolute array 
# time        : [:, 0]         
# pos         : [:, 1,2,3]     - world frame
# vel         : [:, 4,5,6]  
# orient      : [:, 7,8,9,10]  - world frame
# ang_vel_imu : [:, 11,12,13]  - body frame
# accel_imu   : [:, 14,15,16]  - body frame

# # Indices for Data array 
# time        : [:, 0]         
# pos         : [:, 1,2,3]     - body frame
# vel         : [:, 4,5,6]  
# orient      : [:, 7,8,9,10]  - body frame
# ang_vel_imu : [:, 11,12,13]  - body frame
# accel_imu   : [:, 14,15,16]  - body frame

####################
# HELPER FUNCTIONS
####################
# rotation matrix to quaternion
def rotation_matrix_to_quaternion(R):
    """ Convert a rotation matrix to a quaternion. """
    m00, m01, m02 = R[0, 0], R[0, 1], R[0, 2]
    m10, m11, m12 = R[1, 0], R[1, 1], R[1, 2]
    m20, m21, m22 = R[2, 0], R[2, 1], R[2, 2]
    tr = m00 + m11 + m22

    if tr > 0:
        S = np.sqrt(tr+1.0) * 2  # S=4*qw
        qw = 0.25 * S
        qx = (m21 - m12) / S
        qy = (m02 - m20) / S
        qz = (m10 - m01) / S
    elif (m00 > m11) and (m00 > m22):
        S = np.sqrt(1.0 + m00 - m11 - m22) * 2  # S=4*qx
        qw = (m21 - m12) / S
        qx = 0.25 * S
        qy = (m01 + m10) / S
        qz = (m02 + m20) / S
    elif m11 > m22:
        S = np.sqrt(1.0 + m11 - m00 - m22) * 2  # S=4*qy
        qw = (m02 - m20) / S
        qx = (m01 + m10) / S
        qy = 0.25 * S
        qz = (m12 + m21) / S
    else:
        S = np.sqrt(1.0 + m22 - m00 - m11) * 2  # S=4*qz
        qw = (m10 - m01) / S
        qx = (m02 + m20) / S
        qy = (m12 + m21) / S
        qz = 0.25 * S
    return np.array([qw, qx, qy, qz])

# quaternion conjegate ~ inverse operation
def quaternion_conjugate(q):
    """ Returns the conjugate of a quaternion. """
    w, x, y, z = q
    return np.array([w, -x, -y, -z])

# quaternion multiplication
def quaternion_multiplication(q1, q2):
    """ Multiply two quaternions. """
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])

# convert quaternion to rotation matrix
def quaternion_to_rotation_matrix(q):
    """ Convert a quaternion to a rotation matrix. """
    qw, qx, qy, qz = q
    R = np.array([
        [1 - 2*qy**2 - 2*qz**2, 2*qx*qy - 2*qz*qw, 2*qx*qz + 2*qy*qw],
        [2*qx*qy + 2*qz*qw, 1 - 2*qx**2 - 2*qz**2, 2*qy*qz - 2*qx*qw],
        [2*qx*qz - 2*qy*qw, 2*qy*qz + 2*qx*qw, 1 - 2*qx**2 - 2*qy**2]
    ])
    return R

# rotate vector by quaternion
def rotate_vector_by_quaternion(v, q):
    """ Rotate vector v by quaternion q. """
    vq = np.array([0] + v.tolist())
    q_conj = quaternion_conjugate(q)
    # Rotate vector: (q * vq) * conj(q)
    qvq = quaternion_multiplication(q, vq)
    rotated_vq = quaternion_multiplication(qvq, q_conj)

    return rotated_vq[1:]

# Compute transformed delta position
def compute_delta_position(q_from, p_from, p_to):
    # Rotate p_to into the frame of q_from
    rotated_p_to = rotate_vector_by_quaternion(p_to, q_from)
    rotated_p_from = rotate_vector_by_quaternion(p_from, q_from)
    # Compute delta position in the rotated frame
    delta_position = rotated_p_to - rotated_p_from
    return delta_position

def load_logged_data():

    data = np.load('./log/full_states_refactored_with_imu_square.npy', allow_pickle=True).item()
    
    return data

if __name__ == "__main__":

    # loading the data
    logged_data = load_logged_data()
    
    # extract data
    time_array     = logged_data['time']
    gyro_readings  = logged_data['gyro_readings']
    accel_readings = logged_data['accel_readings'] 
    state_array    = logged_data['state']

    # Combine all data
    state_array[:,13:16] = accel_readings
    state_array[:,10:13] = gyro_readings

    # Contains pos,vel,quats in world frame, accels, angVels in body frame
    data_array_for_absolute = np.hstack((time_array.reshape(-1, 1), state_array))

    # true acceleration and angular velocity values
    # acceleration_array = state_array[:,13:16]
    # ang_vel_array = state_array[:,10:13]

    ##############################################
    # Making Positions and Orientations Relative
    ##############################################
    position_array    = state_array[:,:3] 
    orientation_array = state_array[:,6:10]

    # Compute rotations for each quaternion
    rotation_matrices = np.array([quaternion_to_rotation_matrix(q) for q in orientation_array])

    # computing delta positions and delta orientations in quaternion space
    delta_positions = np.array([compute_delta_position(orientation_array[i], position_array[i], position_array[i+1])
                                for i in range(len(position_array)-1)])
    delta_positions = np.vstack((np.zeros((1, delta_positions.shape[1])), delta_positions))

    delta_orientations = np.array([quaternion_multiplication(quaternion_conjugate(orientation_array[i]), orientation_array[i+1])
                                   for i in range(len(orientation_array)-1)])
    delta_orientations = np.vstack((np.array([[1, 0, 0, 0]]), delta_orientations))  # identity quaternion for the first element
    
    # Update state array
    state_array[:, :3] = delta_positions
    state_array[:, 6:10] = delta_orientations

    # make a final post processed data array to be fed for training
    data_array = np.hstack((time_array.reshape(-1, 1), state_array))   
    
    # logged data 
    loggedDict = {'data': data_array,                       # time,pos,vel,quats,angVels,accels in body frame {incremental} 
                  'data_absolute': data_array_for_absolute, # time,pos,vel,quats in world frame, angVels, accels in body frame
                  'state_array': state_array,               # pos, vel, quats in world frame, angVels, accels in body frame
                  'rotation_matrices': rotation_matrices,   # rotation matrices converted from quats in world frame
                  'time': time_array,                       # contains timestamps
                  }

    # saving as npy
    np.save('./log/final_data_absolute_relative_square.npy', loggedDict)
