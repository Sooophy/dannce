#!/bin/bash
#
#SBATCH --job-name=Allcom_pred
#SBATCH --mem=20000                     # Job memory request
#SBATCH -t 6-23:59               # Time limit days-hrs:min:sec
#SBATCH -N 1                         # requested number of nodes (usually just 1)
#SBATCH -n 12                       # requested number of CPUs
#SBATCH -p tdunn       # requested partition on which the job will run
#SBATCH --gres=gpu:1               # gpu:[number_of_requested_gpus]
#SBATCH --exclude=dcc-tdunn-gpu-02,dcc-mastatlab-gpu-01,dcc-gehmlab-gpu-04,dcc-dhvi-gpu-01,dcc-dhvi-gpu-02,dcc-allenlab-gpu-03,dcc-allenlab-gpu-04,dcc-youlab-gpu-01
#SBATCH --output=sophie_predict_all_com.out

: <<'END_COMMENT'
This is a script that looks for the dates in the project folders thatcontains those dates,
copy the io_file and config_file into the project folder, 
and predict com in the project folders.

You need to modify the date_list, and probably also the virtual environment name, io_file, config_file
Make sure io_file, config_file is already in your base folder.
END_COMMENT

set +e
source ~/.bashrc
source activate dannce_stroke

# Base path, have to be an absolute path
base_path="/hpc/group/tdunn/segura-behavior/KE5-7A-1_Aged_female_mice"

# List of dates, You need to modify this list into all the pre-organized project folder
declare -a date_list=("20230427" "20230502" "20230505" "20230512" "20230519" "20230526" "20230602")

# Needed files name, need to modify the name
io_file="io.yaml"
config_file="sophie_com_mouse_config.yaml"

# Loop over each date
for date in "${date_list[@]}"
do
    # Look for directories in the base_path that match the date
    for dir in "$base_path"/*"$date"*
    do
        # Check if the folder exists and it is not the AprilTag folder
        if [ -d "$dir" ] && [[ "$dir" != *"AprilTag"* ]] && [[ "$dir" != *"#"* ]]
        then
            cd "$dir"
            scp ${base_path}/${io_file} ${io_file}
            scp ${base_path}/${config_file} ${config_file}
            # Check if the script is in the directory
            if [ -f "$io_file" ] && [ -f "$config_file" ]
            then
                # Predict and merge
                com-predict-multi-gpu --only-unfinished=True --n-samples-per-gpu=2500 sophie_com_mouse_config.yaml
                com-merge sophie_com_mouse_config.yaml 
                echo "Predict com and merge done in: $dir"
            else
                echo "Predict failed: io_file or config_file missing in: $dir."
            fi
            
            # Go back to the base_path
            cd "$base_path"
            # echo "Go back to: $(pwd)"
        fi
    done
done

