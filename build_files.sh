#!/bin/bash

# Check Python version and ensure pip is available
python --version
python -m pip --version

# Install dependencies
python -m pip install --no-cache-dir -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput
