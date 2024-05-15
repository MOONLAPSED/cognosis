#!/bin/bash
# ==========================================================
# BASH and prompt Configurations
# ==========================================================
# Colored GCC warnings and errors
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'
force_color_prompt=yes
if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        # We have color support; assume it's compliant with Ecma-48
        # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
        # a case would tend to support setf rather than setaf.)
        color_prompt=yes
    else
        color_prompt=
    fi
fi
if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
# Bash history configurations
HISTCONTROL=ignoreboth
HISTSIZE=1000
HISTFILESIZE=2000
shopt -s histappend
# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize


# Check if the shell is running interactively
check_interactive_shell() {
    case "$-" in
        *i*) return 0 ;; # Interactive shell
        *) return 1 ;;   # Non-interactive shell
    esac
}

# Set variable identifying the chroot (if available)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# Function to set up terminal title and color support
setup_terminal() {
    case "$TERM" in
        xterm*|rxvt*)
            PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
            ;;
        *)
            ;;
    esac

    # Enable color support of ls and also add handy aliases
    if [ -x /usr/bin/dircolors ]; then
        test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
        alias ls='ls --color=auto'
        alias grep='grep --color=auto'
        alias fgrep='fgrep --color=auto'
        alias egrep='egrep --color=auto'
    fi

    # Colored GCC warnings and errors
    export GCC_COLORS
}

# Check if terminal setup should be enabled
if [ -n "$ENABLE_TERMINAL_SETUP" ]; then
    setup_terminal
fi

# Color constants for use in scripts and stdout
RED='\033[38;5;255m'
GREEN='\033[38;5;2m'
YELLOW='\033[38;5;214m'
BLUE='\033[38;5;4m'
PURPLE='\033[38;5;127m'

# Function for printing colored text, allowing flexibility
cpick() {
    echo -e "\033[38;5;${1}m${2}\033[0m"
}

# Helper functions for common colors
red() {
    cpick "$RED" "$@"
}
green() {
    cpick "$GREEN" "$@"
}
yellow() {
    cpick "$YELLOW" "$@"
}
blue() {
    cpick "$BLUE" "$@"
}
purple() {
    cpick "$PURPLE" "$@"
}

# Aliases for common commands and Git configurations
alias lll='ls -lka --color=auto'
alias ll='ls -alF --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'
alias ..='../'

# Git aliases for common operations
alias gs='git status'
alias gca='git commit -a'
alias gcam='git commit -am'
alias gp='git push'
alias gup='git pull'
alias gco='git checkout'
alias gcb='git checkout -b'
alias gl='git log --graph --oneline --decorate --all'
alias gll='git log -1 --stat'
alias gclean='git clean -fdX'
alias diff='git diff --color-words'
alias dif='git diff --color --word-diff --stat'

# Git configuration
git config --global rerere.enabled true

# Reverse git add (takes off git add <file> from staging area)
unstage() {
    git reset HEAD -- $1
}

# Enable fsmonitor-watchman deamon for git IPC
git config --global core.fsmonitor true

# Example usage of color functions
echo "$(green "This is green text.")"
echo "$(purple "This is purple text.")"
echo -e "\033[0m" # Reset color to default
# ==========================================================
# Aliases
# ==========================================================
# This section defines various aliases and configurations related to Git.
# Aliases provide shorthand commands for common Git operations, enhancing productivity.
# Additionally, Git functions like enabling rerere and defining a function to unstage changes are configured here.
# ----------------------------------------------------
# Aliases:
# - Various aliases are defined to simplify commonly used Git commands.
#   For example, 'gs' is short for 'git status', 'gca' for 'git commit -a', etc.
# - These aliases can be invoked in the terminal to execute the corresponding Git commands quickly.
# ----------------------------------------------------
# Git Functions:
# - The 'git config' command sets global configurations for Git, such as enabling rerere.
# - The 'unstage' function reverses the 'git add' operation, allowing users to unstage changes from the index.
# ----------------------------------------------------
# Terminal Setup Interaction:
# - The aliases and Git configurations defined here are independent of the terminal setup performed by the `setup_terminal` function.
# - However, if the `ENABLE_TERMINAL_SETUP` variable is set and the `setup_terminal` function is invoked, it will still execute the terminal setup logic.
# - This means that even if aliases and Git configurations are defined, the terminal setup will only occur if explicitly triggered by the `ENABLE_TERMINAL_SETUP` variable.
# - To activate the terminal setup logic, set `ENABLE_TERMINAL_SETUP` to any non-empty value elsewhere in your script.
alias lll='ls -lka --color=auto'
alias ll='ls -alF --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'
alias ..='../'
# alias cr='history | grep <search_term>' # see (reverse-i-search)`' == "ctrl+r" below
# ==========================================================
# git Configurations
# ==========================================================
# Git Aliases
alias gs='git status'
alias gca='git commit -a'
alias gcam='git commit -am'
alias gp='git push'
alias gup='git pull'
alias gco='git checkout'
alias gcb='git checkout -b'
alias gl='git log --graph --oneline --decorate --all'
alias gll='git log -1 --stat'
alias gclean='git clean -fdX'
alias diff='git diff --color-words'
alias dif='git diff --color --word-diff --stat'
# ----------------------------------------------------
# Git Functions
git config --global rerere.enabled 'true'
# reverse git add (takes off git add <file> from staging area)
function unstage() {
  git reset HEAD -- $1
}
# Enable fsmonitor-watchman deamon for git IPC
git config --global core.fsmonitor 'true'
# ==========================================================
# Custom Functions
# ==========================================================
# cr - Reverse search through command history
#
# Usage:
#   cr [PATTERN]
#
# This function allows you to search through your command history in reverse order.
# If no PATTERN is provided, it will search for the last executed command.
# If PATTERN is provided, it will search for commands containing that pattern.
#
# The search results are displayed with line numbers, and you can enter the line
# number to re-execute the corresponding command.
#
# Examples:
#   cr         # Search for the last executed command
#   cr apt     # Search for commands containing the pattern "apt"
#   cr 'apt install'  # Search for commands containing the exact phrase "apt install"
#
cr() {
  if [ $# -eq 0 ]; then
    last_cmd="$(fc -ln -1 | sed "s/^\s*//")"
    if [ -n "$last_cmd" ]; then
      HISTTIMEFORMAT= histunique | grep -i "$last_cmd"
    fi
  else
    HISTTIMEFORMAT= histunique | grep -i "$@"
  fi
  echo -ne "\033[32m(reverse-i-search)\033[0m"': '
}
# ----------------------------------------------------	
# H - Custom command history filtering
#
# Usage:
#   H [PATTERN]
#
# This function filters and sorts the command history based on the provided PATTERN.
# It removes duplicate commands and sorts the output in reverse chronological order.
#
# The function performs the following steps:
#   1. Excludes lines that represent invocations of the `H` function itself.
#   2. Filters the remaining lines based on the provided PATTERN.
#   3. Sorts the output in reverse order based on the second column (command timestamp).
#   4. Removes duplicate lines, considering all fields except the first (line number).
#   5. Performs a final sorting of the output.
#
# If no PATTERN is provided, it will display the entire command history.
#
# Examples:
#   H             # Show the entire command history
#   H apt         # Show commands containing the pattern "apt"
#   H 'apt install'  # Show commands containing the exact phrase "apt install"
#
H() {
    history | egrep -v '^ *[[:digit:]]+ +H +' | grep "$@" | sort -rk 2 | uniq -f 1 | sort
}
# ----------------------------------------------------
# backup - Create a backup copy of a file
#
# Usage:
#   backup FILENAME
#
# This function creates a backup copy of the specified file with the ".bak" extension.
#
# Arguments:
#   FILENAME - The name of the file to be backed up.
#
# Example:
#   backup important_file.txt
#
# This will create a backup copy named "important_file.txt.bak" in the same directory.
#
function backup() {
    cp "$1" "$1.bak"
}

# alert - Notify when a long-running command completes
#
# Usage:
#   command; alert
#
# This alias is used to notify the user when a long-running command completes.
# It prints the last executed command with the prefix "Command completed: ".
#
# To use it, simply append `; alert` to the end of the command you want to monitor.
#
# Example:
#   sleep 10; alert
#
# This will execute the `sleep 10` command and print "Command completed: sleep 10" when it finishes.
#
alias alert='echo "Command completed: $(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'
# ----------------------------------------------------
# popx - Pop multiple directories from the directory stack
#
# Usage:
#   popx NUM
#
# This function pops NUM directories from the directory stack and prints the current
# working directory after the operation.
#
# Arguments:
#   NUM - The number of directories to pop from the stack (must be > 0).
#
# If the directory stack is empty or if NUM is less than or equal to 0,
# an error message is displayed, and the function returns with an error code.
#
# Example:
#   popx 3
#
# This will pop the last 3 directories from the stack and print the current
# working directory after the operation.
#
popx() {
  if [ $# -ne 1 ]; then
    echo "Usage: popx <num>"
    return 1
  fi
  num=$1
  if [ $num -le 0 ]; then
    echo "Error: Number must be > 0"
    return 1
  fi
  for ((i=0; i<num; i++)); do
    if [ ${#DIR_STACK[@]} -eq 0 ]; then
      echo "Error: Directory stack empty"
      return 1
    fi
    popd > /dev/null || break
  done
  pwd
}
# ----------------------------------------------------------
# bp - Backport non-hidden files and directories to parent directory
#
# Usage:
#   bp
#
# This function copies all non-hidden files and directories from the current
# directory to the parent directory.
#
# Example:
#   bp
#
bp() {
    cp -r ./* ../
}

# .bp - Backport all files and directories to parent directory
#
# Usage:
#   .bp
#
# This function copies all files and directories (including hidden ones) from the
# current directory to the parent directory.
#
# After copying the files and directories, it prompts the user to confirm whether
# to delete the current directory if it's empty. If the user confirms, it deletes
# the current directory and changes to the parent directory.
#
# Example:
#   .bp
#
.bp() {
    local current_dir="$(pwd)"
    local parent_dir="$(dirname "$current_dir")"

    # Check if the current directory is not the root directory
    if [[ "$current_dir" == "/" ]]; then
        echo "Cannot move the root directory."
        return 1
    fi

    # Copy all files and directories (including hidden ones)
    shopt -s dotglob # Enable matching dotfiles
    for item in ./*; do
        if [[ -e "$item" ]]; then
            cp -rv --no-preserve=mode "$item" "$parent_dir" || return
            rm -rf "$item"
        fi
    done
    shopt -u dotglob # Disable matching dotfiles

    # Change to the parent directory
    cd "$parent_dir" || return

    echo "All files and directories copied and deleted from the current directory."
}
# ==========================================================
# Init & $PATH
# ==========================================================
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/tp/miniconda/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/tp/miniconda/etc/profile.d/conda.sh" ]; then
        . "/home/tp/miniconda/etc/profile.d/conda.sh"
    else
        export PATH="/home/tp/miniconda/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
# ----------------------------------------------------
#  GO init

# export PATH=$PATH:$HOME/.go/go/bin

#  pipx init
#  .local path init

# export PATH=$PATH:~/.local/bin

# . "$HOME/.cargo/env"

# export PATH=$PATH:~/.cargo/bin

# ==========================================================
# End of Custom Bash Configurations
# ==========================================================
