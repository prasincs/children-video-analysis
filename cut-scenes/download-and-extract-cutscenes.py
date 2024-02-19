#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import csv


parser = argparse.ArgumentParser(description='Download and extract cutscenes from YouTube.')
parser.add_argument('url', help='YouTube URL of the video')
parser.add_argument('-d', '--directory', default='.', help='Directory to save the downloaded and extracted cutscenes')

args = parser.parse_args()

url = args.url
directory = args.directory

# Rest of your code goes here
import subprocess
import subprocess

# Execute yt-dlp command
# this probably could be a library but meh
# -k keeps the intermediate files because yt-dlp is a bit weird and uses webm by default for some videos
ytdlpargs = ['yt-dlp', url, '--remux-video', 'mp4', "-o", "%(title)s-%(id)s.%(ext)s", "--restrict-filename", "-q", "--exec", "./print_sanitized_filename.sh"]
print("running", ' '.join(ytdlpargs))
result = subprocess.run( ytdlpargs, capture_output=True)
if result.returncode != 0:
    print("failed to download video")
    os.exit(1)
filename = result.stdout.strip().decode('utf-8')
print(filename)
if directory != ".":
    destination = os.path.join(directory, filename)
    os.rename(filename, destination)

# Extract the cutscenes
result = subprocess.run(['scenedetect', '-i', f'{filename}', 'detect-adaptive', 'list-scenes', 'save-images'])
# Check if previous command succeeded
if result.returncode != 0:
    print("failed to extract cutscenes")
    os.exit(1)


# Extract the number from the file name
file_name_without_extension = os.path.splitext(filename)[0]
scenes_file = f"{file_name_without_extension}-Scenes.csv"

# Parse the CSV file
with open(scenes_file, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the timecode row
    next(reader)  # skip the header row
    scene_number = sum(1 for row in reader)

# Print the extracted number
print("Extracted scene number:", scene_number)

