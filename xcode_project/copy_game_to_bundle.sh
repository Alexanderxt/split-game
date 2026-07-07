#!/bin/bash
# Copy game HTML/JS/Assets into Xcode project bundle
# Run this from the split-game root directory

GAME_ROOT="/Users/xtmac/Documents/New project/split-game"
XCODE_BUNDLE="$GAME_ROOT/xcode_project/SplitGame/SplitGame"

# Create the bundle directory
mkdir -p "$XCODE_BUNDLE"

# Copy game files
cp "$GAME_ROOT/index.html" "$XCODE_BUNDLE/"
cp "$GAME_ROOT/manifest.json" "$XCODE_BUNDLE/"

# Copy assets
mkdir -p "$XCODE_BUNDLE/assets"
cp "$GAME_ROOT/assets/"*.png "$XCODE_BUNDLE/assets/" 2>/dev/null

echo "Game files copied to Xcode bundle."
echo "Next: open SplitGame.xcodeproj in Xcode and build."
