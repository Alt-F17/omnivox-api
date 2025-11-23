"""
Quick setup script for the Omnivox Python package.

This will check dependencies and environment setup.
"""

import sys
import subprocess
import os


def check_python_version():
    """Check if Python version is 3.8+."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required!")
        return False
    
    print("✅ Python version OK")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    # Get the directory containing this script
    package_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "-e", 
            package_dir
        ])
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def test_import():
    """Test if the package can be imported."""
    print("\n🧪 Testing package import...")
    
    try:
        from omnivox import OmnivoxClient
        from omnivox.exceptions import AuthenticationError
        print("✅ Package imports successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def main():
    """Run setup checks."""
    print("=" * 60)
    print("  Omnivox Python Package - Setup")
    print("=" * 60)
    
    if not check_python_version():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    if not test_import():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Create .env file with your credentials:")
    print("     OMNIVOX_USERNAME=your_student_id")
    print("     OMNIVOX_PASSWORD=your_password")
    print("\n  2. Run the test script:")
    print("     python test_manual.py")
    print("\n  3. Or use in your code:")
    print("     from omnivox import OmnivoxClient")
    print("     client = OmnivoxClient('username', 'password')")
    print()


if __name__ == "__main__":
    main()
