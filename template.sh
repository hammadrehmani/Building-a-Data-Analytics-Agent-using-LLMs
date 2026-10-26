#!/bin/bash

echo "Creating project structure..."

mkdir -p src
mkdir -p static/css
mkdir -p static/js
mkdir -p templates
mkdir -p uploads
mkdir -p charts
mkdir -p logs
mkdir -p research
mkdir -p Dataset

touch app.py
touch requirements.txt
touch .env
touch setup.py

touch src/__init__.py
touch src/agent.py
touch src/helper.py
touch src/prompt.py
touch src/utils.py

touch templates/index.html

touch static/css/style.css
touch static/js/script.js

touch research/trials.ipynb

echo "Project structure created successfully!"
