# Define the URL for the latest release of ExplorerPatcher
$url = "https://github.com/valinet/ExplorerPatcher/releases/latest/download/ep_setup.exe"

# Define the path where the installer will be saved
$output = "$env:TEMP\ep_setup.exe"

# Download the installer
Write-Output "Downloading ExplorerPatcher..."
Invoke-WebRequest -Uri $url -OutFile $output

# Check if the download was successful
if (Test-Path $output) {
    Write-Output "Download complete. Installing ExplorerPatcher..."

    # Run the installer
    Start-Process -FilePath $output -ArgumentList "/silent" -NoNewWindow -Wait

    # Verify installation
    if ($?) {
        Write-Output "ExplorerPatcher installation completed successfully."
    } else {
        Write-Output "ExplorerPatcher installation failed."
    }

    # Optionally, delete the installer after installation
    Remove-Item -Path $output -Force
} else {
    Write-Output "Download failed. Please check your internet connection and try again."
}
