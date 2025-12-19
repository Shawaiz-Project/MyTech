#!/usr/bin/env python
"""
MyTech Website - Local Development Entry Point
Run this file to start the website locally:
    python main.py
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 MyTech Website Starting...")
    print("="*70)
    print("\n📍 Website Available At:")
    print("   Home:       http://localhost:5000/")
    print("   Admin Login: http://localhost:5000/admin/login")
    print("\n🔑 Default Admin Credentials:")
    print("   Username: Shawaiz")
    print("   Password: Shawaiz231980079")
    print("\n⚠️  IMPORTANT: Change password after first login!")
    print("\n⏹️  Press CTRL+C to stop the server")
    print("="*70 + "\n")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
