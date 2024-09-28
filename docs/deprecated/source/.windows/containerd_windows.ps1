# Set constants for paths and URLs
$ContainerdPath = "C:\Program Files\containerd"
$CniBinPath = "$ContainerdPath\cni\bin"
$CniConfPath = "$ContainerdPath\cni\conf"
$NatPluginUrl = "https://github.com/microsoft/windows-container-networking/releases/download/v0.2.0/windows-container-networking-cni-amd64-v0.2.0.zip"
$HnsModuleUrl = "https://raw.githubusercontent.com/microsoft/SDN/master/Kubernetes/windows/hns.psm1"

# Create directories for CNI binaries and configuration
mkdir -Force -Path $CniBinPath
mkdir -Force -Path $CniConfPath

# Download and extract NAT plugin binaries
$NatPluginZip = "$CniBinPath\windows-container-networking-cni-amd64-v0.2.0.zip"
Invoke-WebRequest -Uri $NatPluginUrl -OutFile $NatPluginZip
Expand-Archive -Path $NatPluginZip -DestinationPath $CniBinPath -Force
Remove-Item -Force -Path $NatPluginZip

# Download and import the PowerShell module for network creation
$HnsModule = "$CniBinPath\hns.psm1"
Invoke-WebRequest -Uri $HnsModuleUrl -OutFile $HnsModule
Import-Module -Name $HnsModule

# Define subnet and gateway
$Subnet = "10.0.0.0/16"
$Gateway = "10.0.0.1"

# Create a NAT network if it does not exist
if (!(Get-HnsNetwork | Where-Object { $_.Name -eq "nat" })) {
    New-HNSNetwork -Type Nat -AddressPrefix $Subnet -Gateway $Gateway -Name "nat"
}

# Create containerd network configuration file
$NetworkConfig = @"
{
    "cniVersion": "0.2.0",
    "name": "nat",
    "type": "nat",
    "master": "Ethernet",
    "ipam": {
        "subnet": "$Subnet",
        "routes": [
            {
                "gateway": "$Gateway"
            }
        ]
    },
    "capabilities": {
        "portMappings": true,
        "dns": true
    }
}
"@
Set-Content -Path "$CniConfPath\0-containerd-nat.conf" -Value $NetworkConfig -Force

Write-Host "Containerd network setup complete."