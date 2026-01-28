#!/bin/bash

# Quick Start Script for KC House Price Prediction

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  KC House Price Prediction - Stacking Ensemble          ║"
echo "║  Quick Start Guide                                       ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed"
    echo ""
    echo "Please install Python from: https://www.python.org"
    exit 1
fi

echo "✅ Python found!"
python3 --version
echo ""

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not available"
    exit 1
fi

echo "✅ pip found!"
echo ""

# Install requirements
echo "📦 Installing required packages..."
echo "    (This may take a few minutes on first run)"
echo ""
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Failed to install packages"
    echo "Please check your internet connection"
    exit 1
fi

echo ""
echo "✅ All packages installed successfully!"
echo ""

# Run Streamlit app
echo "🚀 Starting Streamlit application..."
echo ""
echo "    Opening in browser at: http://localhost:8501"
echo ""
echo "📌 To stop the app, press CTRL+C in this window"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

streamlit run streamlit_app.py
