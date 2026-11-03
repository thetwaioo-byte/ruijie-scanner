#!/bin/bash
echo "🚀 Fetching latest Ruijie Scanner from GitHub..."
git pull origin main || git clone https://github.com/thetwaioo-byte/ruijie-scanner.git
cd ruijie-scanner 2>/dev/null || cd ~
python auto_gen_scanner.py
