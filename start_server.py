#!/usr/bin/env python3
"""
Startup script for the Restaurant Recommender System
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required files exist"""
    required_files = [
        'app.py',
        'model.py',
        'zomato_indore.xlsx'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found!")
    return True

def install_dependencies():
    """Install required Python packages"""
    packages = [
        'flask',
        'flask-cors',
        'pandas',
        'numpy',
        'scikit-learn',
        'openpyxl'
    ]
    
    print("📦 Installing required packages...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting Restaurant Recommender Server...")
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")

if __name__ == "__main__":
    print("🍽️ Restaurant Recommender System Startup")
    print("=" * 50)
    
    if not check_requirements():
        print("\nPlease ensure all required files are present.")
        sys.exit(1)
    
    if not install_dependencies():
        print("\nFailed to install dependencies.")
        sys.exit(1)
    
    start_server()
