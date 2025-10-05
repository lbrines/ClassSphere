#!/bin/bash
cd "$(dirname "$0")/src"
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
