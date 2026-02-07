#!/bin/bash

echo "=========================================="
echo "Facebook Marketplace Tenant Agent Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found"

# Install requirements
echo ""
echo "📦 Installing required packages..."
pip install -r requirements.txt --break-system-packages

if [ $? -eq 0 ]; then
    echo "✓ Packages installed successfully"
else
    echo "⚠️  There was an issue installing packages. Trying alternative method..."
    pip install Flask --break-system-packages
fi

# Create templates directory if it doesn't exist
if [ ! -d "templates" ]; then
    echo "⚠️  Templates directory not found. Please ensure all template files are in the 'templates' folder."
fi

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit app.py and update your property details"
echo "2. Run: python3 app.py"
echo "3. Open your browser to http://localhost:5000/test"
echo ""
echo "For detailed instructions, see README.md"
echo ""
