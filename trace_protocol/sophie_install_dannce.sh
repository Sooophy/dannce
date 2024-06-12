###### Install Miniconda ######
yourdirectory="desiredDirectoryName"  # change the name to your folder here, you should manually created this folder already
# mkdir -p /hpc/group/seguralab/"$yourdirectory"
# Download and install a specific version of Miniconda: Miniconda3-py37_4.10.3
cd /hpc/group/seguralab/"$yourdirectory"
echo "Installing Miniconda version 4.10.3..."
wget https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-Linux-x86_64.sh 
sh Miniconda3-py37_4.10.3-Linux-x86_64.sh
# ???? choose path
rm Miniconda3-latest-Linux-x86_64.sh
# Initialize Conda for all future shell sessions
echo "conda installed"

# Activate the base environment
source ~/.bashrc
conda list

# change bash setting
mkdir -p /hpc/group/seguralab/"$yourdirectory"/cache
echo "/hpc/group/seguralab/$yourdirectory" >> ~/.bash_profile

###### Install Dannce ######
cd /hpc/group/seguralab/"$yourdirectory"
git clone --recursive --branch stroke_analysis --single-branch https://github.com/Sooophy/dannce.git
cd dannce
conda create -n dannce_stroke python=3.7 cudatoolkit=10.1 cudnn ffmpeg
conda activate dannce_stroke
conda install pytorch=1.7 -c pytorch
pip install -U setuptools
pip install -e .