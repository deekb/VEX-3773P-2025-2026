#!/bin/bash

# Check if the directories and files exist before executing the commands

# Check if the ./docs directory exists
if [ ! -d "./docs/compiled" ]; then
  echo "The ./docs/compiled directory does not exist, creating it"
  mkdir ./docs/compiled
fi

# Check if the webHelp*.zip file exists
if ls ./webHelp*.zip 1> /dev/null 2>&1; then
  echo "Found a file matching the regex /webHelp*.zip"
else
  echo "Error: The webHelp*.zip file does not exist."
  echo "Make sure to compile your documentation before running this script"
  exit 1
fi

# Check if any files exist in the ./docs/compiled directory
if ls ./docs/compiled 1> /dev/null 2>&1; then
  # Remove files in ./docs directory
  rm -r ./docs/compiled/* &> /dev/null
fi

echo "Extracting files..."
# Unzip the webHelp*.zip file to ./docs directory
unzip -q ./webHelp*.zip -d docs/compiled

echo "Removing zip archive..."

rm ./webHelp*.zip

echo "Done"
