#!/usr/bin/env bash
set -e
echo "=== Installation automatique SUMO (Linux/macOS) ==="
if [ "$(uname)" = "Linux" ]; then
  sudo apt update && sudo apt install -y sumo sumo-tools python3-pip
elif [ "$(uname)" = "Darwin" ]; then
  brew install sumo
else
  echo "Non supporté ici. Utilise install_deps.ps1 pour Windows."
fi
pip3 install -r requirements.txt
echo "Installation terminée. Vérifie avec 'sumo --version'"
