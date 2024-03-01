"""
This script has the following function:
1. Find valid AprilTag folders, copy the params file into project folders. 
   Note that you should name the file correctly as 'YYYYMMDD_big_label3d_dannce.mat'
   and 'YYYYMMDD_big_label3d_dannce.mat' for the big & small cylinder.
2. Create videos folder under each project folder, and move all the videos into that folder.
3. Create COM and DANNCE folder under the project folder.

This script will skip the project folder that already has the params file, 
and regards those folders as already processed.

This script needs further improvement when there are multliple AprilTags folder on the same day!

"""

import os
import scipy.io as sio
import shutil

##### set the path, this is the part you need to modify when using
base_path = '/hpc/group/tdunn/segura-behavior/KE5-7A-1_Aged_female_mice' # The base directory containing all the project folders
# Note: Please name you param file as YYYYMMDD_big_label3d_dannce.mat and YYYYMMDD_small_label3d_dannce.mat, 
# example: 20230509_label3d_dannce.mat, same format with the folder name
params_file_end = '_label3d_dannce.mat' # The camera param file inside of AprilTag folder
filelist = os.listdir(base_path)
# dates_list = ["20230427", "20230502", "20230505", "20230512", "20230519", "20230526", "20230602"]

##### find apriltag with label3d_dannce to find dates
# go over all the folder to find the valid AprilTag folder
# use the AprilTag folder name to find valid experiment dates.
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
