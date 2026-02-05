# SichGate Installation & Setup Guide

## Quick Start (Recommended)

The easiest way to get SichGate running without permission issues:

### macOS / Linux

```bash
# Clone the repository
git clone https://github.com/poshecamo/adversarial-testing-slm-sichgate
cd black-box

# Run the setup script
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source .venv/bin/activate

# Run SichGate
python run_sichgate.py
```

### Windows

```bash
# Clone the repository
git clone https://github.com/poshecamo/adversarial-testing-slm-sichgate
cd black-box

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run SichGate
python run_sichgate.py
```

## What the Setup Script Does

The `setup.sh` script automatically:

1. **Creates a Python virtual environment** - Isolates dependencies
2. **Installs all dependencies** - Ensures correct versions
3. **Fixes HuggingFace cache permissions** - Prevents download errors
4. **Creates a local cache directory** - Fallback if system cache is restricted
5. **Displays next steps** - Shows you exactly what to do

## Troubleshooting

### Issue: "Command not found: python"

**Solution:** Make sure Python 3.8+ is installed:

```bash
python3 --version
# If not installed:
# macOS: brew install python3
# Ubuntu: apt-get install python3
# Windows: Download from python.org
```

### Issue: Permission denied errors

**Solution:** These should be fixed automatically by the setup script. If you still get them:

```bash
# Force cache directory permissions
chmod -R 755 ~/.cache/huggingface

# Or use the local cache (automatically done by the script)
export HF_HOME=$(pwd)/.hf_cache
python run_sichgate.py
```

### Issue: "ModuleNotFoundError: No module named..."

**Solution:** Make sure your virtual environment is activated:

```bash
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

### Issue: Model download fails

**Solution:** The script automatically handles this, but if you still have issues:

```bash
# Use local cache (automatic)
export HF_HOME=$(pwd)/.hf_cache
python run_sichgate.py

# Or use temp cache
export HF_HOME=/tmp/hf_cache
python run_sichgate.py
```

## Manual Installation (Without Setup Script)

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create local cache directory
mkdir -p .hf_cache

# Set cache path
export HF_HOME=$(pwd)/.hf_cache

# Run SichGate
python run_sichgate.py
```

## Permanent Configuration (Optional)

To permanently set the HuggingFace cache location, add to your shell profile:

**macOS/Linux (~/.zshrc or ~/.bash_profile):**

```bash
export HF_HOME=$HOME/.cache/huggingface
```

**Windows PowerShell ($PROFILE):**

```powershell
$env:HF_HOME = "$env:USERPROFILE\.cache\huggingface"
```

Then restart your terminal or run:

```bash
source ~/.zshrc  # or your shell profile
```

## System Requirements

- **Python:** 3.8 or higher
- **RAM:** 4GB minimum (8GB+ recommended for larger models)
- **Storage:** 2-4GB for model downloads (first run only)
- **Internet:** Required for first run to download models

## Verify Installation

Once installed, verify everything works:

```bash
python run_sichgate.py --help
```

You should see the help menu with available options.

## Next Steps

- Read [quickstart.md](quickstart.md) for your first test
- See [readme.md](readme.md) for comprehensive documentation
- Check [usage_examples.py](usage_examples.py) for advanced usage patterns

## Getting Help

If you encounter issues:

1. Check the [readme.md](readme.md) FAQ section
2. Review error messages carefully - they usually indicate the solution
3. Ensure your Python version is 3.8+: `python --version`
4. Make sure your virtual environment is activated
5. Try running with verbose output: `python run_sichgate.py --help`
