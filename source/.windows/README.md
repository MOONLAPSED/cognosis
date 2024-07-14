# /source/.windows/README.md

## windows container routine

First, let's run the `dockerd_windows.ps1` script to start the container:

```powershell
PS C:\path\to\scripts> .\dockerd_windows.ps1
Pulling container image 'ghcr.io/open-webui/open-webui:ollama'...
Pulling container image succeeded.
Running container with options: --detach --publish 3000:8080 --gpus=all --mount type=bind,src=ollama,dst=/root/.ollama --mount type=bind,src=open-webui,dst=/app/backend/data --restart=always
Container started with ID: <container_id>
```

After running this script, the container should be up and running. You can verify this by running `ctr task ls` or `ctr container ls` in your PowerShell terminal.

Now, let's clean up and remove the container by running the `stop_container.ps1` script:

```powershell
PS C:\path\to\scripts> .\stop_container.ps1
Stopping container 'open-webui'...
Container stopped successfully.
Removing container 'open-webui'...
Container removed successfully.
```

Here's a breakdown of what happened:

1. The `stop_container.ps1` script first checked if the `ctr` command was available. If not, it would have exited with an error message.
2. It then used the `ctr task kill` command to stop the running container named `open-webui`.
3. After stopping the container, it used the `ctr container rm` command to remove the stopped container.
4. Finally, it printed a message indicating that the container was stopped and removed successfully.

You can verify that the container is no longer running by running `ctr task ls` or `ctr container ls` again in your PowerShell terminal.

If you need to start the container again, you can simply run `.\dockerd_windows.ps1` once more.

Note: If you want to stop and remove a different container, you'll need to modify the `$containerIdOrName` variable in the `stop_container.ps1` script with the correct container ID or name.


## dockerd_wslubu2204.ps1

```wsl_bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```

User Permissions:

    Ensure the WSL user is part of the docker group to avoid prefacing Docker commands with sudo:

    bash

sudo usermod -aG docker $USER
newgrp docker

### alternative dockerd_____.ps1
`scoop install nonportable/stevedore-np`

A restart may be required, at least on the first install. Please run `sc start stevedored` as an administrator if `docker run` does not work.