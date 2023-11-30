<!---
File: wsl_install_guide.md
Description: Guide for installing and setting up the Windows Subsystem for Linux (WSL).
Note: Follow the steps meticulously for successful installation.
-->
- wsl -d Ubuntu-22.04
cd ~
sudo apt-get update && sudo apt-get upgrade
sudo apt install wget
vi .bashrc 							// add aliases etc
!wq
source .bashrc
wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.5.2-0-Linux-x86_64.sh
chmod +x Miniconda3-py310_23.5.2-0-Linux-x86_64.sh
./Miniconda3-py310_23.5.2-0-Linux-x86_64.sh
exit
wsl -d Ubuntu-22.04
cd ~
conda update conda
conda create -n 3ten python="3.10"
conda install conda
conda install pip
conda update pip
conda deactivate
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash
source .bashrc
nvm                   // check aliases are working and nvm responds then quit
mkdir chrome
cd chrome
sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt install --fix-broken -y
sudo dpkg -i google-chrome-stable_current_amd64.deb
google-chrome         // check chrome is working then quit
// https://ubuntu.com/tutorials/enabling-gpu-acceleration-on-ubuntu-on-wsl2-with-the-nvidia-cuda-platform#2-install-the-appropriate-windows-vgpu-driver-for-wsl
// install nvidia driver on windows if you don't have it but then click "Install NVIDIA CUDA on Ubuntu" on the left-side
sudo apt-get install build-essential && sudo apt-get install manpages-dev
sudo apt install build-essential libglvnd-dev pkg-config
mkdir .nvidia
cd .nvidia            // or wherever you want to install
// download files here per ubuntu.com --> go read the page you can't skip this
sudo ./NVIDIA-Linux-x86_64-535.98.run
sudo apt update -y && sudo apt full-upgrade -y && sudo apt autoremove -y && sudo apt clean -y && sudo apt autoclean -y
nvidia-smi  // double-check nothin is weird 
// https://ubuntu.com/tutorials/enabling-gpu-acceleration-on-ubuntu-on-wsl2-with-the-nvidia-cuda-platform#3-install-nvidia-cuda-on-ubuntu
sudo apt-key del 7fa2af80
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/3bf863cc.pub
sudo add-apt-repository 'deb https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/ /'
sudo apt-get update
sudo apt-get -y install cuda
sudo reboot
wsl --setdefault Ubuntu-22.04
wsl
cd ~
conda activate <envname> (3ten)
pip3 install torch torchvision torchaudio // vanilla
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121   // my fave flavor (rtx3080 on ryzen 5600x)
conda install cudatoolkit (conda env is active)
# ---
git clone https://github.com/oobabooga/text-generation-webui
cd text-generation-webui
pip install -r requirements.txt
pip install bitsandbytes==0.38.1
// RUN echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/lib/' >> ~/.bashrc
// export LD_LIBRARY_PATH=/usr/lib/wsl/lib:/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
// https://github.com/oobabooga/text-generation-webui/issues/400
Start over
conda deactivate
conda remove -n textgen --all
conda create -n textgen python=3.10.9
conda activate textgen
pip3 install torch torchvision torchaudio
cd text-generation-webui
pip install -r requirements.txt
cd /home/yourname/miniconda3/envs/textgen/lib/python3.10/site-packages/bitsandbytes/
cp libbitsandbytes_cuda120.so libbitsandbytes_cpu.so
cd -
python server.py --listen --model llama2.7b.llongma.ggml_v3.q4_K_M.bin --lora alpaca-lora-7b  --load-in-8bit
# ---
// https://localai.io/basics/getting_started/
git clone https://github.com/go-skynet/LocalAI
cd LocalAI
cp your-model.bin models/
docker-compose up -d --pull always
// docker-compose down --volumes - periodically 
// docker run --rm -ti --gpus all -p 8080:8080 -e DEBUG=true -e MODELS_PATH=/models -e PRELOAD_MODELS='[{"url": "github:go-skynet/model-gallery/openllama_7b.yaml", "name": "gpt-3.5-turbo", "overrides": { "f16":true, "gpu_layers": 35, "mmap": true, "batch": 512 } } ]' -e THREADS=1 -e BUILD_TYPE=cublas -v $PWD/models:/models quay.io/go-skynet/local-ai:v0.19.0-cublas-cuda12
