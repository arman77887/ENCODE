#!/bin/bash
# Haq Cyber Squad Auto Installer

echo "🚀 Installing Haq Cyber Squad Banner..."

# Current directory store করুন
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Banner file এর path
BANNER_PATH="$SCRIPT_DIR/haq_banner.py"

# Check if banner file exists
if [ ! -f "$BANNER_PATH" ]; then
    echo "❌ Error: haq_banner.py not found in $SCRIPT_DIR"
    exit 1
fi

# Execute permission দিন
chmod +x "$BANNER_PATH"

# Backup existing .profile
if [ -f ~/.profile ]; then
    cp ~/.profile ~/.profile.backup.$(date +%Y%m%d_%H%M%S)
    echo "📦 Existing .profile backed up"
fi

# Check if already installed
if grep -q "haq_banner.py" ~/.profile; then
    echo "⚠️  Banner already installed in .profile"
else
    # Add to .profile
    echo "" >> ~/.profile
    echo "# Haq Cyber Squad Auto Banner - $(date)" >> ~/.profile
    echo "if [ -f \"$BANNER_PATH\" ]; then" >> ~/.profile
    echo "    python3 \"$BANNER_PATH\"" >> ~/.profile
    echo "fi" >> ~/.profile
    echo "✅ Auto-start added to .profile"
fi

echo ""
echo "🎉 Installation Completed!"
echo "📁 Banner Path: $BANNER_PATH"
echo "🔧 Restart terminal or run: source ~/.profile"
echo "🎯 Test with: python3 \"$BANNER_PATH\""
