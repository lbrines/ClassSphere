#!/bin/bash
while true; do
    if [ ! -f ".next/prerender-manifest.js" ]; then
        mkdir -p .next
        echo "{}" > .next/prerender-manifest.js
        echo "$(date): Created prerender-manifest.js"
    fi
    sleep 1
done
