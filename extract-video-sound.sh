#!/bin/bash

# Check if the input file name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <input_file>"
  exit 1
fi

input_file="$1"

# Extract the base name without extension
base_name=$(basename "$input_file" .mp3)


# extract video to output sound
ffmpeg -i "$input_file" -map 0:a -acodec libmp3lame "${base_name}.mp3"

echo "Processed successfully."

