# -*- coding: utf-8 -*-
"""
This script is used to check segment length, including di1 to dis4, as described below.

dis1: distance between left ear and right ear
dis2: distance between start of spine and end of spine
dis3: distance of left hind paws
dis4: distance of right hind paws

"""

import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio




def calculate_dis(pts1, pts2, pts_location):
    '''
    Parameters
    pts1, pts2: two markers' id that you want to calculate distance between them.
    pts_location : array that contains label3d data

    Returns
    temp_dis : array that contains the distance between pts1 and pts2, unit: mm

    '''
    
    count = pts_location.shape[0]
    temp_dis = np.zeros((count))
    i = 0
    for pts in pts_location:
        if np.isnan(pts[0,pts1]):
            continue
        temp_dis[i] = ((pts[0,pts1] - pts[0,pts2]) ** 2 + \
            (pts[1,pts1] - pts[1,pts2]) ** 2 + (pts[2,pts1] - pts[2,pts2]) ** 2) ** 0.5  
        i = i + 1

    return temp_dis


if __name__ == '__main__':
    
    base_path = '/hpc/group/tdunn/segura-behavior/KE5-3A-1_DANNCE_2-0' # path containing all the folder.
    save_path = base_path + '/check_seg_length_twd5/' # path that will save the results
    pred_mat = 'smoothed_prediction_twd5_nomedfilt.mat' # name of the prediction result

    # params_file_end = 'big_label3d_dannce.mat' # camera parameters
    # Check if the savePath exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # ground truth according to true labels
    ground_truth_average = [19.18, 50.93, 10.59, 10.8]
    ground_truth_std = [2.9, 8, 2.36, 2.48]
    labels = ['BetweenEars', 'Trunk', 'LeftHind', 'RightHind']
    filelist = os.listdir(base_path)
    ##### Use known dates
    # date_ls = ["20230503"]
    date_ls = ["20230503","20230508","20230511","20230518","20230525","20230601","20230616","20230629"]
    for filename in filelist:
        if not os.path.isdir(base_path+'/'+filename):
            continue
        for date in date_ls:
            # if the date is in the folder name and the folder is not AprilTag, find the com file, calculate and plot
            if date in filename and 'AprilTag' not in filename:
                temp_pred_mat = base_path + '/' + filename + '/' + pred_mat
                print(filename)

                if not os.path.exists(temp_pred_mat):
                    print(temp_pred_mat)
                    print("no prediction file")
                    continue

                pre = sio.loadmat(temp_pred_mat)['pred']
                pre_dis1 = calculate_dis(0, 1, pre)
                pre_dis2 = calculate_dis(3, 5, pre)
                pre_dis3 = calculate_dis(16, 17, pre)
                pre_dis4 = calculate_dis(19, 20, pre)
                
                pred_average = [np.mean(pre_dis1), np.mean(pre_dis2), np.mean(pre_dis3), np.mean(pre_dis4)]
                pred_std = [np.std(pre_dis1), np.std(pre_dis2), np.std(pre_dis3), np.std(pre_dis4)]
            
                size = 4
                total_width, n = 0.5, 2
                x = np.arange(size)
                width = total_width / n
                x = x - (total_width - width) / 2
                plt.bar(x, ground_truth_average,  width=width, tick_label=labels, yerr=ground_truth_std, label='GroundTruth')
                plt.bar(x + width, pred_average, width=width, tick_label=labels, yerr=pred_std, label='Prediction')
                plt.legend(loc=1)
                plt.title(filename)
                save_name = save_path + filename + '.jpg'
                plt.savefig(save_name)
                plt.clf()
            # break
                # except:
                #     print('error: '+filename)
                #     continue
    
    # filelist = os.listdir(base_path)
    # for filename in filelist:
    #     if not os.path.isdir(base_path+'/'+filename):
    #         continue
    #     filename_content = os.listdir(base_path+'/'+ filename)
    #     # if it is not a valid AprilTag folder, skip the date
    #     params_file = filename[:8] + params_file_end
    #     if params_file not in filename_content or "AprilTag" not in filename:
    #         continue
    #     # print(params_file)
    #     print("found AprilTag folder: ", filename)
    #     apriltag_file = filename
    #     del filename
    # ##### find project folders
    #     for filename in filelist:
    #         # if the date is in the folder name and the folder is not AprilTag, find the com file, calculate and plot
    #         if apriltag_file[:9] in filename and 'AprilTag' not in filename:
    #             try:    
    #                 temp_pred_mat = base_path + '/' + filelist[j] + '/' + pred_mat
    #                 pre = sio.loadmat(temp_pred_mat)['pred']
    #                 pre_dis1 = calculate_dis(0, 1, pre)
    #                 pre_dis2 = calculate_dis(3, 5, pre)
    #                 pre_dis3 = calculate_dis(16, 17, pre)
    #                 pre_dis4 = calculate_dis(19, 20, pre)
                    
    #                 pred_average = [np.mean(pre_dis1), np.mean(pre_dis2), np.mean(pre_dis3), np.mean(pre_dis4)]
    #                 pred_std = [np.std(pre_dis1), np.std(pre_dis2), np.std(pre_dis3), np.std(pre_dis4)]
                
    #                 size = 4
    #                 total_width, n = 0.5, 2
    #                 x = np.arange(size)
    #                 width = total_width / n
    #                 x = x - (total_width - width) / 2
    #                 plt.bar(x, ground_truth_average,  width=width, tick_label=labels, yerr=ground_truth_std, label='GroundTruth')
    #                 plt.bar(x + width, pred_average, width=width, tick_label=labels, yerr=pred_std, label='Prediction')
    #                 plt.legend(loc=1)
    #                 plt.title(filelist[j])
    #                 save_name = save_path + filelist[j] + '.jpg'
    #                 plt.savefig(save_name)
    #                 plt.clf()
    #             except:
    #                 print('error'+filelist[j])
    #                 continue

    
    
    
    
    # temp_pred_mat = 'C:/lsh/lab/metric_qualify_prediction/20220128_w8c1m1c_smoothed_prediction_twd.mat'
    # pre = sio.loadmat(temp_pred_mat)['pred']
    # ground_truth_average = [19.18, 50.93, 10.59, 10.8]
    # ground_truth_std = [2.9, 8, 2.36, 2.48]
        
    # pre_dis1 = calculate_dis(0, 1, pre)
    # pre_dis2 = calculate_dis(3, 5, pre)
    # pre_dis3 = calculate_dis(16, 17, pre)
    # pre_dis4 = calculate_dis(19, 20, pre)
    
    # pred_average = [np.mean(pre_dis1), np.mean(pre_dis2), np.mean(pre_dis3), np.mean(pre_dis4)]
    # pred_std = [np.std(pre_dis1), np.std(pre_dis2), np.std(pre_dis3), np.std(pre_dis4)]
    # #%%
    # labels = ['BetweenEars', 'Trunk', 'LeftHind', 'RightHind']
    # size = 4
    # total_width, n = 0.5, 2
    # x = np.arange(size)
    # width = total_width / n
    # x = x - (total_width - width) / 2
    # plt.bar(x, ground_truth_average,  width=width, tick_label=labels, yerr=ground_truth_std, label='GroundTruth')
    # plt.bar(x + width, pred_average, width=width, tick_label=labels, yerr=pred_std, label='Prediction')
    # plt.legend(loc=1)