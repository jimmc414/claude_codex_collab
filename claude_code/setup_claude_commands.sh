#!/bin/bash

# Setup Claude Code Global Commands
# This script copies all Claude Code custom commands to the global location

echo "==================================="
echo "Claude Code Global Commands Setup"
echo "==================================="

# Create global commands directory if it doesn't exist
echo "Creating ~/.claude/commands directory if needed..."
mkdir -p ~/.claude/commands

# Define source directory
SOURCE_DIR="/mnt/c/python/claude_codex_collab/claude_commands"
TARGET_DIR="$HOME/.claude/commands"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory not found at $SOURCE_DIR"
    exit 1
fi

# Copy all command files
echo "Copying command files to global location..."
cp "$SOURCE_DIR"/*.md "$TARGET_DIR/"

# Show what was copied
echo ""
echo "Commands installed:"
echo "-------------------"
for file in "$TARGET_DIR"/*.md; do
    if [ -f "$file" ]; then
        basename="${file##*/}"
        command="${basename%.md}"
        echo "  /$command - $(grep -m 1 \"description:\" \"$file\" | sed 's/description: //')"
    fi

done

# Verify installation
echo ""
echo "Verifying installation..."
count=$(ls -1 "$TARGET_DIR"/*.md 2>/dev/null | wc -l)
echo "$count commands successfully installed in $TARGET_DIR"

echo ""
echo "Available Claude Code commands:"
ls -la "$TARGET_DIR"

echo ""
echo "==================================="
echo "Setup Complete"
echo "==================================="
echo ""
echo "To use these commands:"
echo "1. Restart Claude Code with: claude --dangerously-skip-permissions"
echo "2. Use commands like: /github, /push, /pull, /sync, /describe"
echo ""
echo "For a full list of commands in Claude Code, type: /help"
