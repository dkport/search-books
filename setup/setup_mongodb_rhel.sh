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

# Pull MongoDB image
echo "Pulling MongoDB Docker image..."
docker pull mongo:latest

# Run MongoDB container
echo "Starting MongoDB container..."
docker run --name mongodb -d -p 27017:27017 -v ~/mongodb_data:/data/db mongo:latest

echo "MongoDB is up and running on port 27017."

