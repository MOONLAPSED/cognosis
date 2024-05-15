powershell:
 - upgrade to release windows from the flashstick-version .iso (use shift f-10 for command prompt): 
 
       `https://www.microsoft.com/en-us/software-download/windows11` and use the .exe while offline to get new service pack instead of .iso-installed version.
 - download explorer-patcher for tolerable explorer UI:

       `https://github.com/valinet/ExplorerPatcher`
 - if it still doesn't work, hack the registry:

       `https://www.wisecleaner.com/think-tank/389-How-to-Enable-Explorer-Tabs-on-Windows-11-22H2.html`
 - install windows terminal, vscode-insiders, curl, hurl, scoop, micromamba, etc.

        included `.bat` is a good starting-point for customization
 - scoop applications

        `scoop.ps1` is a good starting-point for customization
 - `Invoke-WebRequest -Uri https://aka.ms/wslubuntu2204 -OutFile Ubuntu.appx -UseBasicParsing`
 - `Add-AppxPackage Ubuntu.appx`
 - `wsl --update`
 - `wsl --set-default-version 2`
 - `wsl --install -d Ubuntu-22.04`
 - `wsl --setdefault Ubuntu-22.04`

wsl:
 - `cd ~`
 - `sudo apt update -y && sudo apt full-upgrade -y && sudo apt autoremove -y && sudo apt clean -y && sudo apt autoclean -y`
 - `sudo apt-get install build-essential && sudo apt-get install manpages-dev`
 - `sudo apt install build-essential libglvnd-dev pkg-config`
 - `sudo apt install --fix-broken -y`
 - `wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash`
 - `sudo apt install --fix-broken -y`
 - `mkdir chrome`
 - `cd chrome`
 - `sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb`
 - `sudo dpkg -i google-chrome-stable_current_amd64.deb`
 - """`which google-chrome-stable` make a sym-link in ~/chrome/""" `ln -s /usr/bin/google-chrome-stable ~/chrome/google-chrome`
 - `cd ..` 
 - `mkdir .nvidia`
 - `cd .nvidia`
 - `sudo apt-key del 7fa2af80`
 - `wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin`
 - `sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600`
 - `sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/3bf863cc.pub`
 - `sudo add-apt-repository 'deb https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/ /'`
 - `sudo apt-get update`
 - `sudo apt-get -y install cuda`
 - `sudo reboot`
 - `pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121`
#### only after doing all of the above should you proceed to install conda or mess with systems python3
 - `curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`
 - `bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda`
 - `echo 'export PATH="$HOME/miniconda/bin:$PATH"' >> ~/.bashrc`
 - `source .bashrc`
 - `conda install conda`
 - `conda init bash`
 - `exit`
#### conda --version to confirm, then proceed
 - `wsl shutdown`
 - `wsl`
 - `cd ~`
 - `conda create -n 3ten python="3.10"`
 - `conda activate 3ten`
 - `conda install pip`
 - `pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121`
 - `conda install cudatoolkit`
#### git
 - `ssh-keygen -t rsa -b 4096 -C <your_git_email>`
 - `eval "$(ssh-agent -s)"`
 - `ssh-add ~/.ssh/id_rsa`
 - """copy to clipboard, paste in github as new key""" `xclip -sel clip < ~/.ssh/id_rsa.pub`
 - `ssh -T git@github.com`
 - `echo ".ssh/" >> .gitignore`
 - `git remote set-url origin git@github.com:<username>/<repository>.git`
#### pipx+pdm=>pyproject.toml
 - `pip install pdm`
 - `pip install pipx`


#### Windows11 OCR
https://learn.microsoft.com/en-us/windows/powertoys/text-extractor

    snipping tool OCR char recognition native in-windows eng-US (admin powershell):
    $Capability = Get-WindowsCapability -Online | Where-Object { $_.Name -Like 'Language.OCR*en-US*' }
    $Capability | Remove-WindowsCapability -Online
