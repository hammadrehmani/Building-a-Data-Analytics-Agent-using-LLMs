#!/bin/bash

echo "Creating project structure..."

mkdir -p src
mkdir -p static/css
mkdir -p static/js
mkdir -p templates
mkdir -p uploads
mkdir -p charts
mkdir -p logs

touch app.py
touch requirements.txt
touch .env
touch setup.py

touch src/__init__.py
touch src/agent.py
touch src/utils.py

touch templates/index.html

touch static/css/style.css
touch static/js/script.js

echo "Project structure created successfully!"