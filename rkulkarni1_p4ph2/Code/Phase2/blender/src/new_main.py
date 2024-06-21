"""
main.py
    Simulates the UAV dynamics, cameras and visualizes output
    This entrypoint file runs within Blender's python interpreter

    How to setup Blender and Blender python interpreter?
        Install Blender (this code was tested on version 3.6)

        Ubuntu is officially supported. In case you are using Windows or Mac, these instructions may or may not work
              
        1. Find the python interpreter location associated with the Blender:
            a. Open Blender interactive console within Blender
            b. import sys
            c. print(sys.executable) 
        2. Use pip to install the dependencies from command prompt/terminal (I dont think it worked with powershell though). It will throw a warning and install to something called user site
            "python path" -m pip install imath numpy opencv-python scipy pyquaternion
            For example,
            Windows command looks like this,
                "C:\Program Files\Blender Foundation\Blender 3.6\3.6\python\bin\python.exe" -m pip install opencv-python ...
            Linux command looks like this in my setup,
                /usr/bin/python3.10 -m pip install opencv-python ...
        3. Reopen blender

    How to run the script?
        Create a folder called outputs and open main.blend file
        Goto scripting tab, associate it with main.py if not done already
        Run the script. It takes about 10 seconds to execute
        Goto animation tab and press space to see the visualization
    
    Based on Prof. Nitin's work https://umdausfire.github.io/teaching/fire298/asn3.html
"""

import bpy
import sys
import site

# PATH CONFIGURATION
user_site_packages =site.getusersitepackages()
sys.path.append(user_site_packages) #For pip installed dependencies
sys.path.append('./src')
sys.path.append('/home/pear_group/rutwik/P4/vio/lib/python3.10/site-packages')
sys.path.append('/home/pear_group/rutwik/P4/blender-sim-main/src')


# IMPORT PIP LIBS
import importlib
import math
import os
import random
import numpy as np
import cv2
import scipy
#import OpenEXR
    
# IMPORT DYNAMICS, CONTROL and USER CODE
import quad_dynamics as qd
import control
import tello
import frame_utils as frame
import rendering
import usercode

# Force reload custom modules and run the latest code
importlib.reload(control)
importlib.reload(qd)
importlib.reload(tello)
importlib.reload(frame)
importlib.reload(rendering)
importlib.reload(usercode)

def main():
    # for debugging use print() and blender console.
    #bpy.ops.wm.console_toggle()
    
    # CONSTANTS
    fps = 20

    # STOP time for simulation
    sim_stop_time = 15

    # INIT RENDERING AND CONTROL
    controller = control.quad_control()
    user_sm = usercode.state_machine()
    rendering.init() 
    bpy.context.scene.render.fps = fps
    bpy.context.scene.frame_end = fps*sim_stop_time

    # SET TIME STEP
#    dynamics_dt = 0.01 # og
    dynamics_dt = 0.01 # changed
    control_dt = controller.dt
    user_dt = user_sm.dt
    frame_dt = 1./fps
#    frame_dt = 0.01

    # INIT STATES
    current_time = 0.
#    xyz = np.array([0.0, 0.0, -0.2])
#    vxyz = np.array([0.0, 0.0, 0.0])
#    quat = np.array([1.0, .0, .0, .0])
#    pqr = np.array([0.0, .0, .0])
    
    # Initial States are at Origin {TODO: acceleration at xyz}
    xyz = np.array([0.0, 0.0, 0.0]) # position in xyz
    vxyz = np.array([0.0, 0.0, 0.0]) # velocity in xyz
    quat = np.array([1.0, 0.0, 0.0, 0.0]) # rotation in xyz
    pqr = np.array([0.0, 0.0, 0.0]) # angular rate at xyz
     
    current_ned_state = np.concatenate((xyz, vxyz, quat, pqr))    
    current_ned_state_derivative = np.concatenate((xyz, vxyz, quat, pqr)) 
    
    # INIT TIMER
    dynamics_countdown = 0.
    control_countdown = 0.
    frame_countdown = 0.
    user_countdown = 0.
    
    # INIT LOG
    stateArray = current_ned_state
    stateArray_derivative = current_ned_state_derivative
    timeArray = 0
    controlArray = np.array([0., 0, 0, 0])

    # SCHEDULER SUPER LOOP
    # --------------------------------------------------------------------------------------------
    while current_time < sim_stop_time:

        if frame_countdown<=0.:
            rendering.stepBlender(current_ned_state)
            frame_countdown = frame_dt

        if user_countdown<=0.:
            
            xyz_ned = current_ned_state[0:3] # current position in ned
            xyz_blender = [xyz_ned[0], -xyz_ned[1], -xyz_ned[2]] # current position in blender
            
            vxyz_ned = current_ned_state[3:6] # current vel in ned
            vxyz_blender = [vxyz_ned[0], -vxyz_ned[1], -vxyz_ned[2]] # current vel in blender

        
            # getting desired pos, vel, acc and yaw from usercode in blender frame
            xyz_bl_des, vel_bl_des, acc_bl_des, yaw_bl_setpoint = user_sm.step(current_time, xyz_blender, vxyz_blender)
            
            # Setting desired in blender to desired in ned
            yaw_ned = -yaw_bl_setpoint
            WP_ned = np.array([xyz_bl_des[0], -xyz_bl_des[1], -xyz_bl_des[2], yaw_ned])
            vel_ned = np.array([vel_bl_des[0], -vel_bl_des[1], -vel_bl_des[2]])
            acc_ned = np.array([acc_bl_des[0], -acc_bl_des[1], -acc_bl_des[2]])
                        
            user_countdown = user_dt

        if control_countdown<=0.:
            U = controller.step(current_ned_state, WP_ned, vel_ned, acc_ned)
            control_countdown = control_dt

        # Dynamics runs at base rate. 
        #   TODO replace it with ODE4 fixed step solver
        current_ned_state = current_ned_state + dynamics_dt*qd.model_derivative(current_time,
                                                            current_ned_state,
                                                            U,
                                                            tello)
#       
#        # state vector in ned frame.  
#        delta = qd.model_derivative(current_time, current_ned_state, U, tello)
#        current_ned_state = current_ned_state + dynamics_dt * delta
#        current_ned_state_derivative = delta 
         
        # UPDATE COUNTDOWNS AND CURRENT TIME
        dynamics_countdown -= dynamics_dt
        control_countdown  -= dynamics_dt
        frame_countdown    -= dynamics_dt
        user_countdown     -= dynamics_dt
        current_time       += dynamics_dt

        ############
        # LOGGING
        ############
        # state array is stored in ned frame. 
        stateArray = np.vstack((stateArray, current_ned_state))
#        stateArray_derivative = np.vstack((stateArray_derivative, current_ned_state_derivative)) 
        
        controlArray = np.vstack((controlArray, U))
        timeArray = np.append(timeArray, current_time)
    # ----------------------------------------------------------------------------------------------
    user_sm.terminate()
    
    # SAVE LOGGED SIGNALS TO MAT FILE FOR POST PROCESSING IN MATLAB
    loggedDict = {'time': timeArray,
                  'state': stateArray,
#                  'state_derivatives': stateArray_derivative,
                  'control': controlArray}  
    
    # saving in a .mat file for matlab. 
#    scipy.io.savemat('./log/states_with_acc.mat', loggedDict)
    # saving in a .npy file for python
#    np.save('./log/states_with_acc.npy', loggedDict)
    
if __name__=="__main__":
    # donot run main.py if imported as a module
    main()
    
    
    
     