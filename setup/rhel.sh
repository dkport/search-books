#!/bin/bash

# Update package index
sudo yum update -y

# Install Docker if not installed
if ! [ -x "$(command -v docker)" ]; then
  echo "Installing Docker..."
  sudo yum install -y docker
  sudo systemctl start docker
  sudo systemctl enable docker
fi

