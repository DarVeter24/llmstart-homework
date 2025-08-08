#!/bin/bash
echo "Stopping bot..."
pgrep -f "python.*main.py" | xargs -r kill
echo "Bot stopped" 