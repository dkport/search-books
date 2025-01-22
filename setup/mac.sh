#!/bin/bash

# Detect if running on macOS
if [[ "$(uname)" != "Darwin" ]]; then
  echo "This script is intended for macOS (Darwin)."
  exit 1
fi

# Check if Homebrew is installed
if ! [ -x "$(command -v brew)" ]; then
  echo "Homebrew is not installed. Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  # Add Homebrew to PATH (for immediate use in the script)
  eval "$(/opt/homebrew/bin/brew shellenv || /usr/local/bin/brew shellenv)"
fi

# Install Docker if not installed
if ! [ -x "$(command -v docker)" ]; then
  echo "Installing Docker via Homebrew..."
  brew install --cask docker
  echo "Docker installed. Please start Docker Desktop manually to complete the setup."
  open /Applications/Docker.app
fi

# Wait for Docker to start
echo "Waiting for Docker to start..."
while ! docker info >/dev/null 2>&1; do
  sleep 5
  echo "Docker is still starting..."
done
