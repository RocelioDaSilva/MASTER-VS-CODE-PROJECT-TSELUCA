#!/usr/bin/env bash
set -e

if command -v apt >/dev/null 2>&1; then
  sudo apt update
  sudo apt install -y syncthing
  echo "Syncthing installed (apt). Start it with: syncthing &"
elif command -v pacman >/dev/null 2>&1; then
  sudo pacman -Syu --noconfirm syncthing
  echo "Syncthing installed (pacman). Start it with: syncthing &"
else
  echo "Please install Syncthing using your distribution's package manager or visit https://syncthing.net/downloads/"
fi

# Run syncthing in background for the current user
if command -v syncthing >/dev/null 2>&1; then
  syncthing &
  echo "Syncthing started in background. Open http://127.0.0.1:8384"
fi
