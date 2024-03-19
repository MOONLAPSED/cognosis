#!/bin/bash
# =========================================================
# Custom Bash Configurations
# ==========================================================
# ==========================================================
# Terminal Configurations
# ==========================================================
# colored GCC warnings and errors
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'
# ----------------------------------------------------
# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias dir='dir --color=auto'
    # alias vdir='vdir --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi
# ----------------------------------------------------
# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth
# ----------------------------------------------------
# append to the history file, don't overwrite it
shopt -s histappend
# ----------------------------------------------------
# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000
# ----------------------------------------------------
# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize
# ----------------------------------------------------
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
# ----------------------------------------------------
# If this is an xterm set the title to user@host:dir:
  # `case "$TERM" in` initiates a case statement based on the value of the TERM environment variable
  # xterm*|rxvt*): This is the pattern being matched. It checks if the TERM variable starts with "xterm" or "rxvt"
  # `PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"` sets the terminal title and updates the prompt (PS1)
  # `\[\e]0;...\a\]` uses ANSI escape codes to modify the terminal title. It sets the title to include the user, host, and current
  # directory. The ${debian_chroot:+($debian_chroot)} part is used to include the chroot environment if it's available
  # \u is replaced by the username.
  # \h is replaced by the hostname.
  # \w is replaced by the current working directory.
  # $PS1 is the existing prompt string. The whole expression is appended to the existing prompt.
  # ;; marks the end of the case block.
  # * is a wildcard pattern that matches any other cases
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac
# ----------------------------------------------------
# Color constants for use in scripts and stdout
# Note: 255 corresponds to red in 256-color palette (ANSI escape sequences)
RED='\033[38;5;255m'
GREEN='\033[38;5;2m'
YELLOW='\033[38;5;214m'
BLUE='\033[38;5;4m'
PURPLE='\033[38;5;127m'

# Function for printing colored text, allowing flexibility
# Usage: cpick <color_code> <text>
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
# Example usage of color functions
echo "$(green "This is green text.")"
echo "$(purple "This is purple text.")"
echo -e "\033[0m" # Reset color to default
# ==========================================================
# Aliases
# ==========================================================
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
git config --global rerere.enabled true
# reverse git add (takes off git add <file> from staging area)
function unstage() {
  git reset HEAD -- $1
}
# core.fsmonitor = true  # enable fsmonitor-watchman deamon for git IPC
# ==========================================================
# Custom Functions
# ==========================================================
# Reverse search through command history
cr() {
  if [ $# -eq 0 ]; then
    HISTTIMEFORMAT= history | perl -ne 'print if !$last || $last != $_' | grep -i "$(fc -ln -1 | sed "s/^\s*//")"
  else  
    HISTTIMEFORMAT= history | perl -ne 'print if !$last || $last != $_' | grep -i "$1"
  fi
  echo -ne "\033[32m(reverse-i-search)\033[0m"': ' 
}
# ----------------------------------------------------	
# H() function: Custom command history filtering
H() {
    # This command filters and sorts command history based on criteria provided to the function
    history | egrep -v '^ *[[:digit:]]+ +H +' | grep "$@" | sort -rk 2 | uniq -f 1 | sort;
}
# Explanation of the H() function:
# - `egrep -v '^ *[[:digit:]]+ +H +': This part filters out lines that match the pattern `^[[:digit:]]+ +H +`
# - `grep "$@": Filters the remaining lines based on arguments provided to the H function
# - `sort -rk 2`: Sorts the output in reverse order based on the second column
# - `uniq -f 1`: Removes duplicate lines, considering all fields except the first
# - Final `sort`: Performs a final sorting of the output
# ----------------------------------------------------
# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac
# case $- in: This starts a case statement that checks the value of the shell options stored in the special 
# variable $- The variable $- contains a string of currently set shell options
# *i*) ;;: This line is the first pattern in the case statement. It checks if the value of $- contains the letter "i" 
# (indicating that the shell is running interactively). If pattern matches, double semicolon (;;) indicates that no action is made
# *) return;;: This is the default pattern. If the value of $- does not contain the letter "i", the script returns and does nothing
# ----------------------------------------------------
# backup() function: Create a backup copy of a file
# The backup() function creates a backup copy of a file with a ".bak" extension
function backup() {
    cp "$1" "$1.bak"
}
# Explanation of the backup() function:
# - The $1 refers to the first argument passed to the function (the filename you want to back up)
# - $1.bak represents the backup filename with the ".bak" extension
# - cp "$1" "$1.bak" copies the original file to the backup filename
# ----------------------------------------------------
# Add an "alert" alias for long running commands.  Use like so: `sleep 10; alert`
alias alert='echo "Command completed: $(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'
# ----------------------------------------------------
# Usage: popx <num>
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
    popd > /dev/null 
  done
  pwd
}
# Validates <num> is greater than 0, Loops <num> times popping off the stack with popd, prints pwd
# ----------------------------------------------------
# (reverse-i-search)`' == "ctrl+r"
# to expand the functionality use: `history | grep <search_term>`
# see aliases
# ==========================================================
# Init & $PATH
# ==========================================================
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/tp/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/tp/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/tp/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/tp/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
# ----------------------------------------------------
# NVM init
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
export PATH="/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.1/bin:$PATH"
export PATH="/mnt/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.1:$PATH"
# ----------------------------------------------------
#  GO init
export PATH=$PATH:$HOME/.go/go/bin
#  pipx init
#  .local path init
export PATH=$PATH:~/.local/bin
. "$HOME/.cargo/env"
export PATH=$PATH:~/.cargo/bin
# ==========================================================
# End of Custom Bash Configurations
# ==========================================================
