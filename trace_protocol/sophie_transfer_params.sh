#!/bin/bash
#
# Inputs: com_config - path to com config.
# Example: sbatch sihan_train_com.sh /path/to/com_config.yaml
#SBATCH --job-name=com_pred
#SBATCH --mem=20000                     # Job memory request
#SBATCH -t 6-23:59               # Time limit days-hrs:min:sec
#SBATCH -N 1                         # requested number of nodes (usually just 1)
#SBATCH -n 12                       # requested number of CPUs
#SBATCH -p scavenger-gpu       # requested partition on which the job will run
#SBATCH --gres=gpu:1               # gpu:[number_of_requested_gpus]
#SBATCH --exclude=dcc-tdunn-gpu-01,dcc-tdunn-gpu-02
#SBATCH --output=sophie_transfer_params.out

: <<'END_COMMENT'
This scipt is for predict com in one project folder. Please put this file in the organized project folder and sbatch the script.
Note that you may have to change the virtual environment name to yours.
END_COMMENT

set -e
source ~/.bashrc
source activate dannce_stroke


module load Matlab/R2020b

# Base path, have to be an absolute path
base_path="/hpc/group/tdunn/segura-behavior/KE5-7A-1_Aged_female_mice"
params="camera_params.mat"

# List of dates, You need to modify this list into all the pre-organized project folder
declare -a date_list=("20230427" "20230502" "20230505" "20230512" "20230519" "20230526" "20230602")

# Loop over each date
for date in "${date_list[@]}"
do
    # Look for directories in the base_path that match the date
    for dir in "$base_path"/*"$date"*
    do
        # Check if the folder exists and it is not the AprilTag folder
        if [ -d "$dir" ] && [[ "$dir" == *"AprilTag"* ]] && [ -f "$dir/$params" ]
        then
            echo "$dir"
            cd "$dir" 
            params_path="$dir"/"$params"
            echo "$params_path"
            big_path="$dir"/"$date""_label3d_dannce.mat"
            echo "$big_path"
            # small_path="$dir"/"$date""_small_label3d_dannce.mat"
            # echo "$small_path"
            # small_path=="${$dir}/{$date}_small_label3d_dannce.mat"
            # matlab -batch "clear; total_frames=30000; params_path = '$params_path'; big_path = '$big_path'"

            # total_frames=30000  # not going to work iin a function

            matlab -batch "clear; addpath('$base_path'); total_frames='$total_frames'; params_path = '$params_path'; out_path = '$big_path'; transferParams(params_path,params_path,out_path,22)"
    
            # Go back to the base_path
            cd "$base_path"
            # echo "Go back to: $(pwd)"s
        fi
    done
done

echo "transfer params done"

