#!/bin/bash

# Update package index
sudo apt update -y

# Install Docker if not installed
if ! [ -x "$(command -v docker)" ]; then
  echo "Installing Docker..."
  sudo apt install -y docker.io
  sudo systemctl start docker
  sudo systemctl enable docker
fi
