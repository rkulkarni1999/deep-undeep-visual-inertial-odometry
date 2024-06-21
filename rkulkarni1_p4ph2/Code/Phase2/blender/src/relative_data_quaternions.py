import numpy as np

####################################
# HELPER FUNCTIONS FOR QUATERNIONS
####################################

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

def rotation_matrix_to_euler_angles(R):
    
    # Yaw, Pitch, Roll
    psi = np.arctan2(R[1, 0], R[0, 0])
    theta = np.arcsin(-R[2, 0])
    phi = np.arctan2(R[2, 1], R[2, 2])
    
    roll = np.degrees(phi)
    pitch = np.degrees(theta)
    yaw = np.degrees(psi)
    
    return roll, pitch, yaw

##################
# MAIN
##################
# Define positions
p1 = np.array([0, 2, -1])
p2 = np.array([0, 4, 2])
p3 = np.array([0, 6, 2])
p4 = np.array([0, 10, -10])

# Define orientation matrices {only for converting to quaternions}
R1 = np.array([[0, 0, 1],
               [0, 1, 0],
               [-1, 0, 0]])
R2 = np.array([[0, 0, -1],
               [0, -1, 0],
               [-1, 0, 0]])
R3 = np.array([[0, 0, -1],
               [0, -1, 0],
               [-1, 0, 0]])
R4 = np.array([[0, 0, -1],
               [1, 0, 0],
               [0, -1, 0]])

# Convert rotation matrices to quaternions
q1 = rotation_matrix_to_quaternion(R1)
q2 = rotation_matrix_to_quaternion(R2)
q3 = rotation_matrix_to_quaternion(R3)
q4 = rotation_matrix_to_quaternion(R4)

# Compute quaternion deltas
delta_q1_to_q2 = quaternion_multiplication(quaternion_conjugate(q1), q2)
delta_q2_to_q3 = quaternion_multiplication(quaternion_conjugate(q2), q3)
delta_q3_to_q4 = quaternion_multiplication(quaternion_conjugate(q3), q4)

# Transform positions to local coordinate frames and compute differences
delta_p1_to_p2_quat = compute_delta_position(q1, p1, p2)
delta_p2_to_p3_quat = compute_delta_position(q2, p2, p3)
delta_p3_to_p4_quat = compute_delta_position(q3, p3, p4)

# quats converted to rotation matrix for visual inspection
delta_R1_to_R2_quat = quaternion_to_rotation_matrix(delta_q1_to_q2)
delta_R2_to_R3_quat = quaternion_to_rotation_matrix(delta_q2_to_q3)
delta_R3_to_R4_quat = quaternion_to_rotation_matrix(delta_q3_to_q4)

###################
# Output results
###################
print("(FROM QUATERNIONS) Position from World to 1:", p1)
print("(FROM QUATERNIONS) Position from 1 to 2:", np.round(delta_p1_to_p2_quat, decimals=3))
print("(FROM QUATERNIONS) Position from 2 to 3:", np.round(delta_p2_to_p3_quat, decimals=3))
print("(FROM QUATERNIONS) Position from 3 to 4:", np.round(delta_p3_to_p4_quat, decimals=3))

print("(FROM QUATERNIONS) Orientation from World to 1:\n", rotation_matrix_to_euler_angles(R1))
print("(FROM QUATERNIONS) Orientation from 1 to 2:\n", np.round(rotation_matrix_to_euler_angles(delta_R1_to_R2_quat),decimals=3))
print("(FROM QUATERNIONS) Orientation from 2 to 3:\n", np.round(rotation_matrix_to_euler_angles(delta_R2_to_R3_quat),decimals=3))
print("(FROM QUATERNIONS) Orientation from 3 to 4:\n", np.round(rotation_matrix_to_euler_angles(delta_R3_to_R4_quat),decimals=3))
