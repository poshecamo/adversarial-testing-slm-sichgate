#!/bin/bash
# SichGate Setup Script
# Handles environment configuration and dependency installation

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         SichGate Setup & Configuration                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Create cache directory with proper permissions
echo "🗂️  Setting up HuggingFace cache directory..."
mkdir -p ~/.cache/huggingface
chmod 755 ~/.cache/huggingface

# Fix any permission issues
if [ -d ~/.cache/huggingface ]; then
    chmod -R u+w ~/.cache/huggingface 2>/dev/null || true
fi

# Create local cache directory as fallback
echo "📁 Creating local cache directory..."
mkdir -p ./.hf_cache
export HF_HOME="$(pwd)/.hf_cache"
chmod 755 ./.hf_cache

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ✓ Setup Complete!                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate the environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Run SichGate:"
echo "   python run_sichgate.py"
echo ""
echo "Optional: To use HuggingFace models without cache issues, add"
echo "this to your shell profile (~/.zshrc, ~/.bash_profile, etc):"
echo ""
echo "   export HF_HOME=\$HOME/.cache/huggingface"
echo ""
