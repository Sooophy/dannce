import sys
import os
import numpy as np
import scipy.io as sio
import imageio
from tqdm import tqdm
from projection import *
import pandas as pd
import seaborn as sns
import scipy.signal as signal
import matplotlib.pyplot as plt


def cal_paws_dis(radius, paws_prediction, circle_center):
    
    left_paws = radius - ((paws_prediction[:,0,0] - circle_center[0]) ** 2 + (paws_prediction[:,1,0] - circle_center[1]) ** 2) ** 0.5
    right_paws = radius - ((paws_prediction[:,0,1] - circle_center[0]) ** 2 + (paws_prediction[:,1,1] - circle_center[1]) ** 2) ** 0.5    
    
    left_count = left_paws < 15
    right_count = right_paws < 15
    
    return left_paws, right_paws, left_count, right_count

def binary_threshold(array, window_size, step_size, threshold, peak_value):
    # Padding the array with edge values
    pad_size = window_size // 2
    padded_array = np.pad(array, (pad_size, pad_size), mode='edge')

    # Initialize the result array with zeros
    result = np.zeros_like(array)

    # Iterate with a sliding window
    for i in range(0, len(array), step_size):
        start_index = i
        end_index = start_index + window_size

        # Check if the window is within the bounds of the padded array
        if end_index <= len(padded_array):
            window = padded_array[start_index:end_index]
            # Check if more than 60% of the values in the window are above the threshold
            if np.mean(window > threshold) > 0.7:
                # Set the middle element to threshold
                # Ensure the index is within the bounds of the result array
                middle_index = min(i + pad_size, len(array) - 1)
                result[middle_index] = peak_value
            else:
                # Set the middle element to 0
                # Ensure the index is within the bounds of the result array
                middle_index = min(i + pad_size, len(array) - 1)
                result[middle_index] = 0

    return result



def cal_duration(pred, circle_center, radius, rear_h_thres=0):
    '''
    INPUT:
        pred_path
        circle_center [x,y], xy are coordinates for circle
        radius is the radius of the cylinder, unit mm
        rear_h_thres is threshold for high enough
        rear_d_thres is threshold for distance
        
    OUTPUT:
        result_list = ['left_contact_dur', 'right_contact_dur']
        result_names_list contains all names in the result
    '''
    result_names_list = ['left_contact_dur', 'right_contact_dur']

    hands_prediction = pred[:,:,[8,12]]
    left_distance_all, right_distance_all, left_close, right_close = cal_paws_dis(radius, hands_prediction, circle_center)

    sides = ['left','right']
    # results_list = [] # order should be left_high, left_mid, right_high, right_mid
    for side in sides:
        if side == 'left':
            distance_data = left_distance_all
            heights_data = hands_prediction[:,2,0]
        elif side == 'right':
            distance_data = right_distance_all
            heights_data = hands_prediction[:,2,1]     

        peak_value = 10
        high = binary_threshold(heights_data, window_size=10, step_size=1, threshold=rear_h_thres, peak_value=peak_value) 
        dist_all_filtered = peak_value - binary_threshold(distance_data, window_size=10, step_size=1, threshold=2, peak_value=peak_value)
        contact = high * dist_all_filtered
        contact_dur = np.count_nonzero(contact)
        # breakpoint()

        contact_rate = contact_dur/30000
        if side == 'left':
            left_dur = contact_rate
        elif side == 'right':
            right_dur = contact_rate

    return left_dur, right_dur

pred_mat = '/DANNCE/predict_results/twd5/save_data_MAX.mat'
com_mat = '/DANNCE/predict_results/twd5/com3d_used.mat'
radius = 47.5
bad_pred = ['bad']
# base_path = '/hpc/group/tdunn/segura-behavior/Nhi_exp/'
base_path = '/your_project_folder/'
df_meta = pd.read_csv("path_to_your_metadata.csv")

change_center_list = [] # if you happened to flip your boar by accident, put the folder names here. e.g. "20241015_d7_c3_m4_cylinder"

for (k, row) in tqdm(df_meta.iterrows()):

    project_folder = str(row["Date"]) + "_" + row["Timepoint"] + "_" + row["AnimalID"][:2] + "_" + row["AnimalID"][2:] + "_cylinder"     
    if project_folder in bad_pred:
        print(f"Skipping bad pred: {project_folder}")
        continue
    # for one video visualization
    # if project_folder != "20241015_d7_c3_m4_cylinder":
    #     continue
    prediction_path =  base_path + '/' + project_folder + '/' + pred_mat
    com_path = base_path + '/' + project_folder + '/' + com_mat
    try:
        pred = sio.loadmat(prediction_path)['pred'][:30000]
        # for raw pred
        com = sio.loadmat(com_path)['com'][:30000]
        pred = pred+com[:,:,np.newaxis]
    except FileNotFoundError as error:
        print(error)
        breakpoint()
        continue
    # print(project_folder)
    # left_hand = pred[:, :, 8]
    # right_hand = pred[:, :, 12]

    if project_folder in change_center_list:
        circle_center = [12.7,-13.5]
    else:
        circle_center = [12.7,-19.2]
    
    left_dur, right_dur = cal_duration(pred, circle_center, radius, rear_h_thres=0)
    df_meta.at[k, "left_dur"] = left_dur
    df_meta.at[k, "right_dur"] = right_dur
df_meta.to_csv("duration.csv", index=False)


df_meta = pd.read_csv("duration.csv")

def calculate_laterality_index(row):
    
    return row['right_dur']/(row['left_dur'] + row['right_dur'])
    # return row['right_dur']/row['left_dur']

def process_data(df):
    # Calculate laterality index
    df['laterality_index'] = df.apply(calculate_laterality_index, axis=1)

    ##### uncomment this to normalize data
    # for (k, row) in df.iterrows():
    #     conditions = (
    #         (df['AnimalID'] == row['AnimalID']) &
    #         (df['Timepoint'] == 'd0')
    #     )
    #     df.at[k, "baseline"] = df[conditions]['laterality_index'].iloc[0]
    # df['laterality_index'] = df['laterality_index'] - df['baseline'] 

    grouped = df.groupby(['Condition', 'Timepoint'])['laterality_index']
    stats = pd.DataFrame({
        'mean': grouped.mean(),
        'sem': grouped.sem()
    }).reset_index()
    
    return stats


def plot_laterality_index(stats, timepoint_order):
    """
    Create a line plot with SEM error bars using matplotlib (since we're plotting pre-calculated SEM)
    """
    # Set the style
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))
    
    # Get unique conditions
    conditions = stats['Condition'].unique()
    colors = sns.color_palette("deep", len(conditions))
    
    # Plot for each condition
    for idx, condition in enumerate(conditions):
        condition_data = stats[stats['Condition'] == condition]
        
        # Ensure data is in correct timepoint order
        condition_data = condition_data.set_index('Timepoint').loc[timepoint_order].reset_index()
        
        plt.errorbar(x=range(len(timepoint_order)), 
                    y=condition_data['mean'],
                    yerr=condition_data['sem'],
                    label=condition,
                    color=colors[idx],
                    marker='o',
                    capsize=5,
                    capthick=1,
                    markersize=8,
                    linewidth=2)
    
    # Customize the plot
    # plt.title('Right duration / left duration Over Time', pad=20)
    # plt.xlabel('Time Point')
    # plt.ylabel('right duration/ left duration')

    plt.title('Right duration / total duration Over Time', pad=20)
    plt.xlabel('Time Point')
    plt.ylabel('right duration/ total duration')
    
    # Set custom timepoint order on x-axis
    plt.xticks(range(len(timepoint_order)), timepoint_order)
    
    # Set y-axis limits
    # plt.ylim(-1, 1)
    
    # Add legend
    plt.legend(title='Condition', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Adjust layout to prevent legend cutoff
    plt.tight_layout()
    
    return plt.gcf()

timepoint_order = ['d0', 'd12', 'd33', 'd54']
stats = process_data(df_meta)
fig = plot_laterality_index(stats, timepoint_order)
plt.savefig("duration_raw.png")

breakpoint()