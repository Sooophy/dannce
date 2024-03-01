#!/bin/bash
#
# Inputs: com_config - path to com config.
# Example: sbatch sihan_train_com.sh /path/to/com_config.yaml
#SBATCH --job-name=All_smooth
#SBATCH --mem=20000                     # Job memory request
#SBATCH -t 6-23:59               # Time limit days-hrs:min:sec
#SBATCH -N 1                         # requested number of nodes (usually just 1)
#SBATCH -n 12                       # requested number of CPUs
#SBATCH -p tdunn       # requested partition on which the job will run
#SBATCH --gres=gpu:1               # gpu:[number_of_requested_gpus]
#SBATCH --output=sophie_get_true_label_smooth_all.out

: <<'END_COMMENT'
This is a script that lgettrue labels for the predictions fro tdun MAX model.

You need to modify the date_list. 
And probably you need to change the python file name, also the smoothed result file name.
END_COMMENT

set -e
source ~/.bashrc
source activate dannce_stroke

# Base path, have to be an absolute path
base_path="/hpc/group/tdunn/segura-behavior/KE5-7A-1_Aged_female_mice"
# # This is used to check if the prediction is complete, should have 13 prediction file
# pred_path="DANNCE/predict_results/twd3"

# List of dates, You need to modify this list into all the pre-organized project folder
# declare -a date_list=("20230503")

declare -a date_list=("20230427" "20230502" "20230505" "20230512" "20230519" "20230526" "20230602")

# Needed files name, need to modify the name
pred_file="DANNCE/predict_results/twd5/save_data_MAX.mat"
echo "$pred_file"

# Loop over each date
for date in "${date_list[@]}"
do
    # Look for directories in the base_path that match the date
    for dir in "$base_path"/*"$date"*
    do  
        echo "$dir"
        # Check if the folder exists and it is not the AprilTag folder
        if [ -d "$dir" ] && [[ "$dir" != *"AprilTag"* ]] && [[ "$dir" != *"#"* ]]
        then
            cd "$dir"
            scp ${base_path}/sophie_get_true_label_smooth.py sophie_get_true_label_smooth.py
            if [ ! -f "$pred_file" ]; then 
                echo "Prediction not merged"
                continue
            fi

            python sophie_get_true_label_smooth.py
            # if [ ! -f smoothed_prediction_twd_withmetadata.mat ]; then
            #     echo "generating smoothed file"
            #     python sophie_get_true_label_smooth.py
            # fi

            cd ..
        else
            echo "not a project folder, skip"
        fi
    done
done



