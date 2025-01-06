#!/bin/bash

# Use the first argument if provided, otherwise use the current working directory
search_dir="${1:-$(pwd)}"

# Function to process files recursively
convert_svgs_to_pngs() {
    local dir="$1"
    for file in "$dir"/*; do
        if [ -d "$file" ]; then
            # If the file is a directory, recurse into it
            convert_svgs_to_pngs "$file"
        elif [[ "$file" == *.svg ]]; then
            # If the file is an SVG, render it to PNG
            output="${file%.svg}.png" # Replace .svg with .png
            echo "Rendering $file to $output"
            inkscape "$file" --export-type=png --export-filename="$output"
        fi
    done
}

# Start the recursive process
convert_svgs_to_pngs "$search_dir"
