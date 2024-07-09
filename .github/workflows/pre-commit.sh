#!/bin/bash

shopt -s globstar
for file in **/*.md; do
    dir=$(dirname "$file")
    media_dir="$dir/media"
    if [ ! -d "$media_dir" ]; then
        echo "Error: $dir does not contain a /media/ directory for multimedia files."
        exit 1
    fi
done
