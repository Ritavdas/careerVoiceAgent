"""
Quick setup script for WhatsApp Bot
Run this to install dependencies and create basic structure
"""

import os
import subprocess
import sys


def run_command(cmd):
    """Run a shell command and handle errors"""
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {cmd}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {cmd}")
        print(f"Error: {e.stderr}")
        return None


def main():
    print("🤖 Setting up WhatsApp Bot...")
    print("=" * 50)

    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required for PyWA")
        print(f"Current version: {sys.version}")
        sys.exit(1)

    print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}")

    # Install dependencies
    print("\n📦 Installing dependencies...")
    run_command("pip install -r requirements.txt")

    # Create .env if it doesn't exist
    if not os.path.exists(".env"):
        print("\n📝 Creating .env file from template...")
        run_command("cp .env.example .env")
        print("⚠️  Please edit .env file with your actual values!")
    else:
        print("✅ .env file already exists")

    # Create directories
    directories = ["logs", "uploads", "downloads"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")

    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your WhatsApp API credentials")
    print("2. Get a public URL (use ngrok for testing)")
    print("3. Configure webhook in Meta Developer Console")
    print("4. Run: fastapi dev main.py --port 8000")
    print("\n📚 Check README.md for detailed instructions")


if __name__ == "__main__":
    main()
