import numpy as np
import matplotlib.pyplot as plt
import math

def load_logged_data():
    # Loads the data from the .npy file
    data = np.load('./log/full_states_for_imuSensor.npy', allow_pickle=True).item()
    return data

def quaternion_to_rpy(qw, qx, qy, qz):
    # Calculate the roll (x-axis rotation)
    sinr_cosp = 2 * (qw * qx + qy * qz)
    cosr_cosp = 1 - 2 * (qx * qx + qy * qy)
    roll = math.atan2(sinr_cosp, cosr_cosp)
    
    # Calculate the pitch (y-axis rotation)
    sinp = 2 * (qw * qy - qz * qx)
    if abs(sinp) >= 1:
        # Use 90 degrees if out of range
        pitch = math.copysign(math.pi / 2, sinp)
    else:
        pitch = math.asin(sinp)
    
    # Calculate the yaw (z-axis rotation)
    siny_cosp = 2 * (qw * qz + qx * qy)
    cosy_cosp = 1 - 2 * (qy * qy + qz * qz)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    roll = math.degrees(roll)
    pitch = math.degrees(pitch)
    yaw = math.degrees(yaw)
    
    return roll, pitch, yaw

def compute_angular_acceleration(angular_velocities, time_array):
    # Calculate differences between consecutive angular velocity vectors
    delta_omega = np.diff(angular_velocities, axis=0)
    # Calculate time differences
    delta_time = np.diff(time_array)
    # Angular acceleration is the change in angular velocity divided by the change in time
    angular_accelerations = delta_omega / delta_time[:, np.newaxis]  # make delta_time 2D for broadcasting
    return angular_accelerations


if __name__ == "__main__":
    try:
        # loading the data
        logged_data = load_logged_data()
        
        # timestamps
        time_array = logged_data['time']
        # state data
        full_state = logged_data['state']

        quaternions = full_state[:, 6:10]    
        angular_velocities = full_state[:, 10:13]
        linear_accelerations = full_state[:, 13:16]
        
        # Extracting orientations as roll, pitch, yaw
        euler_angles = np.array([quaternion_to_rpy(qw, qx, qy, qz) for qw, qx, qy, qz in full_state[:, 6:10]])

        # Extracting angular velocities
        angular_velocities = full_state[:, 10:13]
        
        # Extracting linear accelerations
        linear_accelerations = full_state[:, 13:16]

        # compute angular accelerations
        angular_accelerations = compute_angular_acceleration(angular_velocities, time_array)

        # Plotting all data in subplots
        fig, axs = plt.subplots(3, 1, figsize=(10, 18))

        # Plotting converted from 
        axs[0].plot(time_array, euler_angles[:, 0], label='Roll (X-axis)')
        axs[0].plot(time_array, euler_angles[:, 1], label='Pitch (Y-axis)')
        axs[0].plot(time_array, euler_angles[:, 2], label='Yaw (Z-axis)')
        axs[0].set_title('Orientation Angles Over Time')
        axs[0].set_xlabel('Time (s)')
        axs[0].set_ylabel('Angle (degrees)')
        axs[0].legend()
        axs[0].grid(True)

        # Plotting angular velocities
        axs[1].plot(time_array, angular_velocities[:, 0], label=r'$\omega_x$ (rad/s)')
        axs[1].plot(time_array, angular_velocities[:, 1], label=r'$\omega_y$ (rad/s)')
        axs[1].plot(time_array, angular_velocities[:, 2], label=r'$\omega_z$ (rad/s)')
        axs[1].set_title('Angular Velocities Over Time')
        axs[1].set_xlabel('Time (s)')
        axs[1].set_ylabel('Angular velocity (rad/s)')
        axs[1].legend()
        axs[1].grid(True)

        # Plotting linear accelerations
        axs[2].plot(time_array, linear_accelerations[:, 0], label=r'$a_x$ (m/s²)')
        axs[2].plot(time_array, linear_accelerations[:, 1], label=r'$a_y$ (m/s²)')
        axs[2].plot(time_array, linear_accelerations[:, 2], label=r'$a_z$ (m/s²)')
        axs[2].set_title('Linear Accelerations Over Time')
        axs[2].set_xlabel('Time (s)')
        axs[2].set_ylabel('Linear acceleration (m/s²)')
        axs[2].legend()
        axs[2].grid(True)

        # Plotting angular accelerations
        # axs[3].plot(time_array[:-1], angular_accelerations[:, 0], label=r'$\alpha_x$ (rad/s²)')
        # axs[3].plot(time_array[:-1], angular_accelerations[:, 1], label=r'$\alpha_y$ (rad/s²)')
        # axs[3].plot(time_array[:-1], angular_accelerations[:, 2], label=r'$\alpha_z$ (rad/s²)')
        # axs[3].set_title('Angular Accelerations Over Time')
        # axs[3].set_xlabel('Time (s)')
        # axs[3].set_ylabel('Angular acceleration (rad/s²)')
        # axs[3].legend()
        # axs[3].grid(True)

        plt.tight_layout()
        plt.show()

    except KeyboardInterrupt:
        print("Plotting interrupted by user.")
        plt.close()
        raise

    # except KeyboardInterrupt:
    #     print("Plotting interrupted by user.")
    #     plt.close()  # This ensures that the plot window is closed when Ctrl+C is pressed
    #     raise

    # Plot a single quaternion 
    quaternion = full_state[11880, 6:10]
    print(type(quaternion))

    # angular velocities
    angular_velocities = full_state[1, 10:13]
    linear_accelerations = full_state[1, 13:16]


    # RPY in blender frame
    # roll, pitch, yaw = quaternion_to_rpy(quaternion[0], quaternion[1], -quaternion[2], -quaternion[3])
    
    # RPY in NED Frame
    roll, pitch, yaw = quaternion_to_rpy(quaternion[0], quaternion[1], quaternion[2], quaternion[3])

    euler_angle_ned = np.array([roll, pitch, yaw])
    
    # print(f"Roll, Pitch, Yaw in NED Frame: {np.round(euler_angle_ned, decimals=3)}")
    # print(f"Quaternion in NED Frame: {np.round(quaternion, decimals=3)}")