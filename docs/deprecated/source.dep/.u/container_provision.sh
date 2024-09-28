#!/bin/bash

# Script to configure Docker and NFS in a container not to be used in production.

# NFS Configuration

SERVER_IP="192.168.1.10"

echo "Installing NFS server..."
sudo apt-get install -y nfs-kernel-server

echo "Creating a directory for NFS share..."
sudo mkdir /shared

echo "Configuring NFS exports..."
echo "/shared $SERVER_IP(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports

echo "Restarting NFS server..."
sudo systemctl restart nfs-kernel-server

echo "Opening NFS ports in the firewall..."
sudo ufw allow 2049/tcp
sudo ufw allow 2049/udp

# Docker Configuration

echo "Installing Docker..."
sudo apt-get install -y docker.io

echo "Starting a Docker container with NFS volume..."
docker run -v $SERVER_IP:/shared:/cognos_container

echo "Docker and NFS configuration complete."