#!/bin/bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r req.txt

# Collect static files
python manage.py collectstatic --no-input

# Run other build steps if needed