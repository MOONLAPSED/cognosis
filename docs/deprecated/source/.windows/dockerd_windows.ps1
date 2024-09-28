# Set the container image reference
$imageRef = "ghcr.io/open-webui/open-webui:ollama"

# Set the container run options
$runOptions = @(
    "--detach",
    "-p", "3000:8080",
    "--gpus=all",  # Ensure host supports GPU
    "--mount", "type=bind,src=ollama,dst=/root/.ollama",
    "--mount", "type=bind,src=open-webui,dst=/app/backend/data",
    "--restart=always"
)

# Function to check if a command exists
function Test-CommandExists {
    param (
        [string]$Command
    )

    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try {
        if (Get-Command $Command) {
            return $true
        }
    } catch {
        Write-Host "Command '$Command' not found."
        return $false
    } finally {
        $ErrorActionPreference = $oldPreference
    }
}

# Check if ctr command exists
if (-not (Test-CommandExists "ctr")) {
    Write-Host "containerd runtime (ctr) not found. Please install it first." -ForegroundColor Red
    return
}

# Pull the container image for the windows platform
Write-Host "Pulling container image '$imageRef'..."
try {
    & ctr image pull --platform windows/amd64 $imageRef
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Pulled container image successfully." -ForegroundColor Green
    } else {
        Write-Host "Failed to pull container image." -ForegroundColor Red
        return
    }
} catch {
    Write-Host "Failed to pull container image: $($_.Exception.Message)" -ForegroundColor Red
    return
}

# Run the container
Write-Host "Running container with options: $($runOptions -join ' ')"
try {
    $containerId = & ctr run --platform windows/amd64 $runOptions $imageRef
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Container started with ID: $containerId" -ForegroundColor Green
    } else {
        Write-Host "Failed to run container." -ForegroundColor Red
    }
} catch {
    Write-Host "Failed to run container: $($_.Exception.Message)" -ForegroundColor Red
}