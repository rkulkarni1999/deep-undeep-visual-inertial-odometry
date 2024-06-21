import numpy as np

#########################################
# HELPER FUNCTIONS FOR ROTATION MATRIX
########################################
def rotation_matrix_to_euler_angles(R):
    psi = np.arctan2(R[1, 0], R[0, 0])
    theta = np.arcsin(-R[2, 0])
    phi = np.arctan2(R[2, 1], R[2, 2])
    
    roll = np.degrees(phi)
    pitch = np.degrees(theta)
    yaw = np.degrees(psi)
    
    return roll, pitch, yaw

############
# MAIN
############
# Define positions
p1 = np.array([0, 2, -1])
p2 = np.array([0, 4, 2])
p3 = np.array([0, 6, 2])
p4 = np.array([0, 10, -10])

# Define orientation matrices
R0 = np.array([[1, 0, 0],
               [0, 1, 0],
               [0, 0, 1]])
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


# Compute the change in position
# Transform positions to local coordinate frames and compute differences
delta_p1_to_p2 = np.linalg.inv(R1) @ (p2 - p1)
delta_p2_to_p3 = np.linalg.inv(R2) @ (p3 - p2)
delta_p3_to_p4 = np.linalg.inv(R3) @ (p4 - p3)

# Compute the change in orientation
delta_R0_to_R1 = R1
delta_R1_to_R2 = np.linalg.inv(R1) @ R2   # orientation change bw frame {1} and {2} wrt to frame {1}
delta_R2_to_R3 = np.linalg.inv(R2) @ R3
delta_R3_to_R4 = np.linalg.inv(R3) @ R4

print("(FROM ROTATION MATRIX) Rotation from World to 1:", rotation_matrix_to_euler_angles(R1))
print("(FROM ROTATION MATRIX) Rotation from 1 to 2:", rotation_matrix_to_euler_angles(delta_R1_to_R2))
print("(FROM ROTATION MATRIX) Rotation from 2 to 3:", rotation_matrix_to_euler_angles(delta_R2_to_R3))
print("(FROM ROTATION MATRIX) Rotation from 3 to 4:", rotation_matrix_to_euler_angles(delta_R3_to_R4))

a1_world = np.array([0, 1, -1])
a2_world = np.array([0, 1, 1])
a3_world = np.array([0, 0, 1])
a4_world = np.array([0, 1, 1])

o1_world = np.array([0, 1, -1])
o2_world = np.array([0, 1, 1])
o3_world = np.array([0, 0, 1])
o4_world = np.array([0, 1, 1])

# Compute the accelerations in local frames
a1_local = np.linalg.inv(R0) @ a1_world
a2_local = np.linalg.inv(R1) @ a2_world
a3_local = np.linalg.inv(R2) @ a3_world
a4_local = np.linalg.inv(R3) @ a4_world



# Print accelerations in local frames for verification
print("Acceleration from frame {0} to {1}:", a1_local)
print("Acceleration from frame {1} to {2}:", a2_local)
print("Acceleration from frame {2} to {3}:", a3_local)
print("Acceleration from frame {3} to {4}:", a4_local)

# Output results
print("(FROM ROTATION MATRIX) Position from World to 1:", p1)
print("(FROM ROTATION MATRIX) Position from 1 to 2:", np.round(delta_p1_to_p2, decimals=3))
print("(FROM ROTATION MATRIX) Position from 2 to 3:", np.round(delta_p2_to_p3, decimals=3))
print("(FROM ROTATION MATRIX) Position from 3 to 4:", np.round(delta_p3_to_p4, decimals=3))






