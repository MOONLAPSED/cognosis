# for windows:
# https://github.com/valinet/ExplorerPatcher

# Install Git and update Scoop buckets
scoop bucket add versions
scoop bucket add extras
scoop install git
scoop install main/gh
scoop install versions/vscode-insiders
scoop install versions/windows-terminal-preview
scoop install main/eza
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
function RunCommand($command, [bool]$yesToAll = $false) {
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
        Invoke-Expression $command 2>&1 | Tee-Object -FilePath "scoop_log.txt"
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
RunCommand "scoop install main/frp" $yesToAll
RunCommand "scoop install extras/carapace-bin" $yesToAll
RunCommand "scoop install main/yq" $yesToAll
RunCommand "scoop install main/jc" $yesToAll
RunCommand "scoop install extras/chatall" $yesToAll
RunCommand "scoop install main/fq" $yesToAll
RunCommand "scoop install main/zoxide" $yesToAll
RunCommand "scoop install main/nu" $yesToAll
RunCommand "scoop install main/windows-application-driver" $yesToAll
RunCommand "scoop install extras/texteditorpro" $yesToAll
RunCommand "scoop install main/miller" $yesToAll
RunCommand "scoop install main/clink" $yesToAll
RunCommand "scoop install main/clink-flex-prompt" $yesToAll
RunCommand "scoop bucket add nerd-fonts" $yesToAll
RunCommand "scoop install nerd-fonts/FiraMono-NF-Mono" $yesToAll
RunCommand "scoop install nerd-fonts/FiraCode-NF" $yesToAll
RunCommand "scoop install main/fx" $yesToAll
RunCommand "scoop install main/yedit" $yesToAll
RunCommand "scoop install main/bison" $yesToAll
RunCommand "scoop install main/hurl" $yesToAll
RunCommand "scoop install main/fselect" $yesToAll
RunCommand "scoop install main/rcc" $yesToAll
RunCommand "scoop install main/cheat" $yesToAll
RunCommand "scoop install main/navi" $yesToAll
