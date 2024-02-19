#!/bin/bash

# Example of sanitizing the filename (simple version)
sanitized_filename=$(basename $1 | tr ' ' '_' | tr -cd 'A-Za-z0-9_.-')

# Print the sanitized filename
echo "$sanitized_filename"