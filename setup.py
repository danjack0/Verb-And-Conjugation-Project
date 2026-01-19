#!/usr/bin/env python3
"""
Setup script for VerbAndConjProj
Automatically sets up the virtual environment and downloads required models.
"""

import subprocess
import sys
import os
import platform

def run_command(cmd, description):
    """Run a command and print status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Setting up VerbAndConjProj...")
    print("=" * 50)

    # Create virtual environment
    if not run_command("python -m venv .venv", "Creating virtual environment"):
        return False

    # Activate virtual environment
    if platform.system() == "Windows":
        activate_cmd = ".venv\\Scripts\\activate"
    else:
        activate_cmd = "source .venv/bin/activate"

    # Install requirements
    pip_cmd = f"{activate_cmd} && pip install -r requirements.txt"
    if not run_command(pip_cmd, "Installing Python dependencies"):
        return False

    # Download SpaCy model
    spacy_cmd = f"{activate_cmd} && python -c \"import spacy; spacy.cli.download('it_core_news_md')\""
    if not run_command(spacy_cmd, "Downloading SpaCy Italian model"):
        return False

    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nTo run the project:")
    if platform.system() == "Windows":
        print("  .venv\\Scripts\\activate")
    else:
        print("  source .venv/bin/activate")
    print("  python main.py")
    print("\nBuono studio! 📚")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)