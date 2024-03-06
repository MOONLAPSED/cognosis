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
function RunCommand($command) {
    Write-Host "Running command: $command"

    # Confirmation prompt
    while ($true) {
        $confirmation = Read-Host -Prompt "Proceed with installation? (Y/N)"
        if ($confirmation -eq "Y") {
            break  # Proceed with execution
        } elseif ($confirmation -eq "N") {
            Write-Host "Installation skipped."
            return  # Exit the function
        } else {
            Write-Host "Invalid input. Please enter 'Y' or 'N'."
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
RunCommand "scoop update"

# Install required packages
RunCommand "scoop install extras/okular"
RunCommand "scoop install extras/irfanview-lean"
RunCommand "scoop install extras/mpc-hc-fork"
# RunCommand "scoop install main/sourcegraph-cli"
RunCommand "scoop install main/frp"
RunCommand "scoop install extras/carapace-bin"
RunCommand "scoop install main/yq"
RunCommand "scoop install main/jc"
RunCommand "scoop install extras/chatall"
RunCommand "scoop install main/fq"
RunCommand "scoop install main/zoxide"
RunCommand "scoop install main/nu"
# RunCommand "scoop install main/windows-application-driver"
RunCommand "scoop install extras/texteditorpro"
RunCommand "scoop install main/miller"
RunCommand "scoop install main/clink"
RunCommand "scoop install main/clink-flex-prompt"
RunCommand "scoop bucket add nerd-fonts"
RunCommand "scoop install nerd-fonts/FiraMono-NF-Mono"
RunCommand "scoop install nerd-fonts/FiraCode-NF"
RunCommand "scoop install main/fx"
RunCommand "scoop install main/yedit"
RunCommand "scoop install main/bison"
# RunCommand "scoop install main/hurl"
RunCommand "scoop install main/fselect"
RunCommand "scoop install main/rcc"
RunCommand "scoop install main/cheat"
RunCommand "scoop install main/navi"


