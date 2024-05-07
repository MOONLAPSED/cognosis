<#
.SYNOPSIS
This script is designed to install and configure various software tools and utilities on a Windows virtual machine during startup.

.DESCRIPTION
The script performs the following tasks:
1. Installs Git and updates Scoop buckets.
2. Installs various software tools using Scoop, including VSCode Insiders, Windows Terminal Preview, lsd, and mambaforge.
3. Sets the desktop target and adds PATH additions for micromamba and Scoop bin.
4. Launches common applications like Microsoft Edge, Notepad, and Windows Explorer.
5. Updates Scoop and installs additional software packages based on user confirmation.

.NOTES
This script requires Scoop to be installed on the system. It also assumes that the Scoop buckets mentioned in the script are available.

.EXAMPLE
Run the script during the Windows virtual machine startup process.
#>

# Install Git and update Scoop buckets
scoop bucket add versions
scoop bucket add extras
scoop install git
scoop install main/gh
scoop install versions/vscode-insiders
scoop install versions/windows-terminal-preview
scoop install main/lsd
scoop install extras/mambaforge

# Set desktop target and PATH additions (using Environment Variables)
$desktop = "C:\Users\WDAGUtilityAccount\Desktop"
$desktopPath = "$desktop\micromamba;$desktop\Scoop\bin"
$env:PATH = [Environment]::GetEnvironmentVariable("PATH", "User")
$env:PATH += ";$desktopPath"
[Environment]::SetEnvironmentVariable("PATH", $env:PATH, "User")

# Launch common applications
Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
Start-Process "notepad.exe"
Start-Process "explorer.exe"
try {
    Start-Process "wt.exe" -Wait
} catch {
    Start-Process "powershell.exe"
}

# Define the RunCommand function
function RunCommand {
    <#
    .SYNOPSIS
    Runs a command and handles user confirmation and error handling.

    .DESCRIPTION
    The RunCommand function prompts the user for confirmation before executing a command. If the user chooses to proceed with all subsequent commands, the function executes the command without further confirmation. The function also logs the command output to a file named "scoop_log.txt" and handles any errors that may occur during command execution.

    .PARAMETER command
    The command to be executed.

    .PARAMETER yesToAll
    A switch parameter that determines whether to execute all subsequent commands without confirmation.

    .EXAMPLE
    RunCommand "scoop install git"
    RunCommand "scoop update" $true
    #>
    param (
        [Parameter(Mandatory = $true)]
        [string]$command,
        [switch]$yesToAll = $false
    )

    Write-Host "Running command: $command"

    if (-not $yesToAll) {
        # Confirmation prompt
        while ($true) {
            $confirmation = Read-Host -Prompt "Proceed with installation? (Y/N/A)"
            if ($confirmation -eq "Y") {
                break  # Proceed with execution
            } elseif ($confirmation -eq "N") {
                Write-Host "Installation skipped."
                return  # Exit the function
            } elseif ($confirmation -eq "A") {
                $yesToAll = $true
                break  # Proceed with execution for all subsequent commands
            } else {
                Write-Host "Invalid input. Please enter 'Y', 'N', or 'A'."
            }
        }
    }

    # Execute the command and handle potential errors
    try {
        Invoke-Expression $command 2>&1 | Tee-Object -FilePath "scoop_log.txt" -Append
    } catch {
        Write-Error "Command execution failed: $command"
        Write-Error $_.Exception.Message 
    }
}

# Update Scoop
RunCommand "scoop install git" $true  # Running "scoop install git" without confirmation
RunCommand "scoop update" $true  # Running "scoop update" without confirmation

# Setting yesToAll to true for all subsequent commands
$yesToAll = $true  
RunCommand "scoop bucket add nerd-fonts" $yesToAll
RunCommand "scoop bucket add extras" $yesToAll
RunCommand "scoop bucket add versions" $yesToAll
RunCommand "scoop install extras/x64dbg" $yesToAll
RunCommand "scoop install main/curl" $yesToAll
RunCommand "install versions/openssl-light" $yesToAll
RunCommand "scoop install extras/okular" $yesToAll
RunCommand "scoop install extras/irfanview-lean" $yesToAll
RunCommand "scoop install extras/mpc-hc-fork" $yesToAll
RunCommand "scoop install extras/carapace-bin" $yesToAll
RunCommand "scoop install main/zoxide" $yesToAll
RunCommand "scoop bucket add nerd-fonts" $yesToAll
RunCommand "scoop install nerd-fonts/FiraMono-NF-Mono" $yesToAll
RunCommand "scoop install nerd-fonts/FiraCode-NF" $yesToAll
