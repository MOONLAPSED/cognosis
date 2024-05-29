# dockered_wslubu2204.ps1
# This script assumes Docker is set up and running in WSL2 Ubuntu 22.04

# Set the container image reference
$imageRef = "ghcr.io/open-webui/open-webui:ollama"

# Set the container run options
$runOptions = @(
    "-d",
    "-p", "3000:8080",
    "--gpus=all",  # Ensure host supports GPU
    "--add-host=host.docker.internal:host-gateway",
    "--mount", "type=bind,src=/mnt/c/Users/Dev/Documents/cognosis/ollama,dst=/root/.ollama",
    "--mount", "type=bind,src=/mnt/c/Users/Dev/Documents/cognosis/open-webui,dst=/app/backend/data",
    "--restart=always",
    "--name", "open-webui"
)

# Set WSL distribution
$wslDistro = "Ubuntu-22.04"

# Function to run command in WSL
function Invoke-WSLCommand {
    param (
        [string]$Distro,
        [string]$Command
    )
    wsl -d $Distro -- bash -c "$Command" 2>&1 | Out-String
}

# Function to check if Docker is installed
function Test-DockerInstalled {
    param (
        [string]$Distro
    )
    $result = Invoke-WSLCommand -Distro $Distro -Command "docker --version"
    return $result -match "Docker version"
}

# Function to ensure directory exists
function Ensure-DirectoryExists {
    param (
        [string]$Distro,
        [string]$Path
    )
    $result = Invoke-WSLCommand -Distro $Distro -Command "mkdir -p $Path"
    return $result
}

# Display starting message
Write-Host "Starting Docker container within WSL2 ($wslDistro)..."

# Check if Docker is installed
if (-not (Test-DockerInstalled -Distro $wslDistro)) {
    Write-Host "Docker is not installed or not found in the WSL distribution." -ForegroundColor Red
    return
}

# Ensure mount directories exist
Ensure-DirectoryExists -Distro $wslDistro -Path "/mnt/c/Users/Dev/Documents/cognosis/ollama"
Ensure-DirectoryExists -Distro $wslDistro -Path "/mnt/c/Users/Dev/Documents/cognosis/open-webui"

# Pull the container image
Write-Host "Pulling container image '$imageRef'..."
$pullResult = Invoke-WSLCommand -Distro $wslDistro -Command "docker pull $imageRef"

if ($pullResult -notmatch "Status.*Downloaded|Image is up to date") {
    Write-Host "Failed to pull container image. Details: $pullResult" -ForegroundColor Red
    return
}

# Construct the Docker command
$dockerCmd = "docker run " + ($runOptions -join " ") + " " + $imageRef

# Run the Docker container
Write-Host "Running container with options: $($runOptions -join ' ')"
$runResult = Invoke-WSLCommand -Distro $wslDistro -Command $dockerCmd

# Check the result of the container run
If ($runResult -match "error: could not select device driver \".*\" with capabilities:") {
    Write-Host "Failed to run the container: GPU support issue detected. Please ensure NVIDIA drivers and the NVIDIA container toolkit are correctly installed and configured." -ForegroundColor Red
} elseif ($runResult.StartsWith("Error response from daemon")) {
    Write-Host "Failed to run the container: $runResult" -ForegroundColor Red
} else {
    Write-Host "Container started successfully: $runResult" -ForegroundColor Green
}