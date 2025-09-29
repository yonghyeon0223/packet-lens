#!/bin/bash

set -e

echo "🔧 Installing required system packages..."
sudo apt update
sudo apt install -y tshark python3 python3-venv python3-pip

# Step 2: Create project directory and virtual environment
PROJECT_DIR="$HOME/Projects/packet-lens"
VENV_DIR="$PROJECT_DIR/venv"

echo "📁 Creating project directory at $PROJECT_DIR..."
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

echo "🐍 Creating virtual environment..."
python3 -m venv "$VENV_DIR"

# Step 3: Activate virtual environment and install squarify
echo "📦 Activating virtual environment and installing python packages..."
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install matplotlib pandas seaborn squarify
python3 src/main.py

# Step 4: Deactivate virtual environment
deactivate
echo "🚪 Virtual environment deactivated. Setup complete!"
