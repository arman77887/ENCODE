#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

def setup_auto_banner():
    # Get current script directory
    script_dir = Path(__file__).parent
    banner_file = script_dir / "auto_update_banner.py"
    
    # Check if banner file exists
    if not banner_file.exists():
        print("❌ Error: auto_update_banner.py not found!")
        return False
    
    # Make banner executable
    banner_file.chmod(0o755)
    
    # Backup existing .profile
    profile_path = Path.home() / ".profile"
    if profile_path.exists():
        backup_path = profile_path.with_suffix(f'.profile.backup.{os.getpid()}')
        profile_path.rename(backup_path)
        print(f"📦 Backup created: {backup_path}")
    
    # Read existing .profile content
    existing_content = ""
    if profile_path.exists():
        existing_content = profile_path.read_text()
    
    # Check if already installed
    if "auto_update_banner.py" in existing_content:
        print("⚠️  Banner already installed in .profile")
        return True
    
    # Add auto-start code
    auto_start_code = f"""
# Crypticx Auto Banner
if [ -f "{banner_file}" ]; then
    python3 "{banner_file}"
fi
"""
    
    # Write to .profile
    with open(profile_path, 'w') as f:
        f.write(existing_content)
        f.write(auto_start_code)
    
    print("✅ Auto-start configured successfully!")
    print(f"📁 Banner path: {banner_file}")
    return True

def test_banner():
    """Test the banner installation"""
    script_dir = Path(__file__).parent
    banner_file = script_dir / "auto_update_banner.py"
    
    if banner_file.exists():
        print("🚀 Testing banner...")
        os.system(f'python3 "{banner_file}"')
    else:
        print("❌ Banner file not found!")

if __name__ == "__main__":
    print("🏴 Crypticx Auto Setup")
    print("═" * 40)
    
    if setup_auto_banner():
        print("\n🎉 Setup completed successfully!")
        print("🔧 Restart your terminal or run: source ~/.profile")
        
        # Ask to test
        test = input("\n🧪 Test banner now? (y/n): ").lower()
        if test == 'y':
            test_banner()
    else:
        print("❌ Setup failed!")
        sys.exit(1)
