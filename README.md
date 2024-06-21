# Deep UnDeep Visual Inertial Odometry

## Phase 1 : Classical Approach to Visual Inertial Odometry

### Introduction

This project provides a Python reimplementation of the Stereo Multi-State Constraint Kalman Filter (S-MSCKF) for visual-inertial odometry. This implementation has been inspired from the C++ implementation by KumarRobotics/msckf_vio. 

### Algorithm Overview

MSCKF (Multi-State Constraint Kalman Filter) is an Extended Kalman Filter (EKF) based, tightly-coupled visual-inertial odometry algorithm. S-MSCKF is the stereo version of MSCKF. This algorithm is designed to provide robust and accurate visual-inertial odometry, especially for applications requiring fast and autonomous flight.

### Key Papers:

- Robust Stereo Visual Inertial Odometry for Fast Autonomous Flight by Ke Sun et al. (2017)
- A Multi-State Constraint Kalman Filter for Vision-aided Inertial Navigation by Anastasios I. Mourikis et al. (2006)

### Requirements
- Python 3.6+
- numpy
- scipy
- cv2
- pangolin (optional, for trajectory/poses visualization)


### Dataset

- This project utilizes the EuRoC MAV dataset, which contains visual-inertial datasets collected onboard a Micro Aerial Vehicle (MAV). The datasets include stereo images, synchronized IMU measurements, and ground-truth data.

### Dataset Details:

- EuRoC MAV: The dataset can be found here.

### Running the Code

- To run the visual-inertial odometry algorithm with visualization, use the following command: 
    ```
    python vio.py --view --path path/to/your/EuRoC_MAV_dataset/MH_01_easy
    ```

- For running the algorithm without visualization, use:
    ```
    python vio.py --path path/to/your/EuRoC_MAV_dataset/MH_01_easy
    ```

- Final Output

![classsical-vio-final-output-gif](https://github.com/rkulkarni1999/deep-undeep-visual-inertial-odometry/assets/74806736/807f8b60-0350-487d-850a-b3ca568cf745)

## Phase 2: Deep Learning Approach to Visual Inertial Odometry

### Problem Statement

![image](https://github.com/rkulkarni1999/deep-undeep-visual-inertial-odometry/assets/74806736/d9f96d9b-3350-4e37-9a2a-25fa6a2a3dd0)

### Dataset Generation using Blender

![deep-vio-data-generation-video](https://github.com/rkulkarni1999/deep-undeep-visual-inertial-odometry/assets/74806736/7133df37-c689-4976-9f36-2e202eb2e9fb)

![image](https://github.com/rkulkarni1999/deep-undeep-visual-inertial-odometry/assets/74806736/97ecc9e3-3080-4def-8501-886420771a16)

### Networks Used 

#### Deep Visual Odometry Network

![image](https://github.com/rkulkarni1999/deep-undeep-visual-inertial-odometry/assets/74806736/3f901056-60c8-42b2-aed1-cd8945802582)

#### Deep Inertial Odometry Network

![image](https://github.com/rkulkarni1999/deep-undeep-visual-inertial-odometry/assets/74806736/98b6094e-c988-4e79-b499-95bdebfa0f00)

#### Deep Visual Inertial Odometry Network

![image](https://github.com/rkulkarni1999/deep-undeep-visual-inertial-odometry/assets/74806736/706475c0-47b0-4a28-82a6-3fccd8dd39c9)


### Final Output [will be uploaded soon]

