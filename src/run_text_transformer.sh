#!/bin/bash
# Script to install dependencies and run the text transformer application

echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully!"
    echo "Starting Text Transformer Application..."
    echo "Press Ctrl+C to exit"
    python text_transformer.py
else
    echo "Failed to install dependencies. Please check your internet connection and try again."
    exit 1
fi