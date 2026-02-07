#!/bin/bash

echo "🚀 Starting deployment..."

# Git pull
echo "📥 Pulling latest code..."
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/Update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements/base.txt

# Run migrations
echo "🗄️ Running migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Restart services
echo "🔄 Restarting services..."
sudo systemctl restart gunicorn
sudo systemctl restart nginx

echo "✅ Deployment completed!"
