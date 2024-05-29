# cleanup.ps1
# This script tears down and cleans up the Docker environment inside WSL2

# Set WSL distribution
$wslDistro = "Ubuntu-22.04"

# Function to run command in WSL
function Invoke-WSLCommand {
    param (
        [string]$Distro,
        [string]$Command
    )
    wsl -d $Distro -- $Command 2>&1 | Out-String
}

# Function to check if a command exists in WSL
function Test-WSLCommandExists {
    param (
        [string]$Distro,
        [string]$Command
    )
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try {
        if (Invoke-WSLCommand -Distro $Distro -Command "command -v $Command") {
            return $true
        }
    } catch {
        return $false
    } finally {
        $ErrorActionPreference = $oldPreference
    }
}

# Stop and remove Docker containers
Write-Host "Stopping and removing Docker containers..."
if (Test-WSLCommandExists -Distro $wslDistro -Command "docker") {
    $containers = Invoke-WSLCommand -Distro $wslDistro -Command "docker ps -aq"
    if ($containers) {
        Invoke-WSLCommand -Distro $wslDistro -Command "docker stop $containers"
        Invoke-WSLCommand -Distro $wslDistro -Command "docker rm $containers"
        Write-Host "Docker containers stopped and removed." -ForegroundColor Green
    } else {
        Write-Host "No running Docker containers to stop." -ForegroundColor Yellow
    }
} else {
    Write-Host "Docker command not found in WSL distribution." -ForegroundColor Red
}

# Stop Docker daemon
Write-Host "Stopping Docker daemon..."
if (Test-WSLCommandExists -Distro $wslDistro -Command "pkill") {
    $daemonStatus = Invoke-WSLCommand -Distro $wslDistro -Command "pkill -f dockerd"
    if (!$daemonStatus) {
        Write-Host "Docker daemon stopped." -ForegroundColor Green
    } else {
        Write-Host "Failed to stop Docker daemon or not running." -ForegroundColor Yellow
    }
} else {
    Write-Host "pkill command not found in WSL distribution." -ForegroundColor Red
}

# Cleanup Docker images and volumes (optional)
Write-Host "Cleaning up Docker images and volumes..."
if (Test-WSLCommandExists -Distro $wslDistro -Command "docker") {
    Invoke-WSLCommand -Distro $wslDistro -Command "docker system prune -af --volumes"
    Write-Host "Docker images and volumes cleaned up." -ForegroundColor Green
} else {
    Write-Host "Docker command not found in WSL distribution." -ForegroundColor Red
}

# Additional process cleanup
Write-Host "Ensuring no leftover processes are running..."
if (Test-WSLCommandExists -Distro $wslDistro -Command "pkill") {
    $leftoverProcesses = Invoke-WSLCommand -Distro $wslDistro -Command "pgrep -f docker"
    if ($leftoverProcesses) {
        Invoke-WSLCommand -Distro $wslDistro -Command "pkill -f docker"
        Write-Host "Leftover Docker processes stopped." -ForegroundColor Green
    } else {
        Write-Host "No leftover Docker processes found." -ForegroundColor Yellow
    }
} else {
    Write-Host "pkill/pgrep commands not found in WSL distribution." -ForegroundColor Red
}

Write-Host "Cleanup complete."