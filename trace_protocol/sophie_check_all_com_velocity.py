"""
This script has the following function:
1. Under the base_path, look for valid project folders with com3d.mat, check if the mat file is compelete. 
2. Generate plots of com velocity and save to save_path

"""


import os
import scipy.io as scio
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

base_path = '/hpc/group/tdunn/segura-behavior/KE5-7A-1_Aged_female_mice' # The base directory containing all the project folders
# Note: Please name you param file as YYYYMMDD_label3d_dannce.mat, 
# example: 20230509_label3d_dannce.mat, same format with the folder name
params_file_end = '_label3d_dannce.mat' # The camera param file inside of AprilTag folder
filelist = os.listdir(base_path)
expected_frame_num = 30000 # expected frame number of com file, 30000 for 5min 100fps on default
save_path = base_path +'/com_check'
# Check if the savePath exists
if not os.path.exists(save_path):
    os.makedirs(save_path)


##### Use known dates
# date_ls = ["20230503"]
date_ls = ["20230427", "20230502", "20230505", "20230512", "20230519", "20230526", "20230602"]
for filename in filelist:
    if not os.path.isdir(base_path+'/'+filename):
        continue
    for date in date_ls:
        # if the date is in the folder name and the folder is not AprilTag, find the com file, calculate and plot
         
         if "#" in filename:
            continue
         if filename == '20230505_w1_c6_m4':
        #  if date in filename and 'AprilTag' not in filename:
            print(filename, ": start analyzing")
            temp_path = base_path + '/' + filename + '/COM/predict_results/com3d.mat'
            try:
                coms = scio.loadmat(temp_path)['com']
                # breakpoint()

                # smooth
                coms = signal.medfilt(coms,(31,1))

            except (FileNotFoundError, IOError):
                print("No prediction found in:", filename)
                continue
            
            # if the frames is less than 30000 (5min, 1000 fps), skip
            if coms.shape[0] < expected_frame_num:
                print(coms.shape[0])
                # print("frames are incomplete!")
                # print(temp_path)
                # continue
                # sys.exit()
            
            plt.subplot(211)
            plt.plot(coms)
            plt.title(filename)
            diff_x=np.diff(coms[:,0])
            diff_y=np.diff(coms[:,1])      
            diff_z=np.diff(coms[:,2])   
            speed = np.power(np.power(diff_x, 2) + np.power(diff_y, 2) + np.power(diff_z, 2) , 1/2)
            
            speed_sat = list(range(200))
            speed_xlabel = np.linspace(0,20,200)
            for k in range(200):
                temp = np.where((speed < (k+1)*0.1)&(speed >= k*0.1))
                speed_sat[k] = temp[0].shape[0]
            
            plt.subplot(212)
            plt.plot(speed_xlabel, speed_sat)
            plt.xlabel('speed, mm/frame')
            plt.ylabel('amount, frames')
            
            # Save rge result to the desired place
            plt.savefig(save_path + filename +'.jpg')
            plt.show()
            plt.clf()
            
            # Theortically the result shouldn't have small waves on the tails after 5 mm/frames        


##### method2: find apriltag with label3d_dannce to find dates
# go over all the folder to find the valid AprilTag folder
# use the AprilTag folder name to find valid experiment dates.
"""
for filename in filelist:
    if not os.path.isdir(base_path+'/'+filename):
        continue
    filename_content = os.listdir(base_path+'/'+ filename)
    # if it is not a valid AprilTag folder, skip the date
    params_file = filename[:8] + params_file_end
    if params_file not in filename_content or "AprilTag" not in filename:
        continue
    # print(params_file)
    print("found AprilTag folder: ", filename)
    apriltag_file = filename
    del filename
##### find project folders
    for filename in filelist:
        # if the date is in the folder name and the folder is not AprilTag, find the com file, calculate and plot
         if apriltag_file[:9] in filename and 'AprilTag' not in filename:
            temp_path = base_path + '/' + filename + '/COM/predict_results/com3d.mat'
            coms = scio.loadmat(temp_path)['com']
            
            # if the frames is less than 30000 (5min, 1000 fps), skip
            if coms.shape[0] < 30000:
                print("frames are incomplete!")
                print(temp_path)
                sys.exit()
            
            plt.subplot(211)
            plt.plot(coms)
            plt.title(filelist[j])
            diff_x=np.diff(coms[:,0])
            diff_y=np.diff(coms[:,1])      
            diff_z=np.diff(coms[:,2])   
            speed = np.power(np.power(diff_x, 2) + np.power(diff_y, 2) + np.power(diff_z, 2) , 1/2)
            
            speed_sat = list(range(200))
            speed_xlabel = np.linspace(0,20,200)
            for k in range(200):
                temp = np.where((speed < (k+1)*0.1)&(speed >= k*0.1))
                speed_sat[k] = temp[0].shape[0]
            
            plt.subplot(212)
            plt.plot(speed_xlabel, speed_sat)
            plt.xlabel('speed, mm/frame')
            plt.ylabel('amount, frames')
            
            # Save rge result to the desired place
            plt.savefig(save_path + filename +'.jpg')
            plt.show()
            plt.clf()
            
            # Theortically the result shouldn't have small waves on the tails after 5 mm/frames        
""" 