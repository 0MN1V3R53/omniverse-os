#!/bin/bash
# Omniverse SEO Daemons Launcher

echo "Stopping any existing SEO daemons..."
pkill -f "continuous_seo_deployment_daemon.py" || true
pkill -f "seo_30min_keyword_engine.py" || true

echo "Starting Continuous SEO Deployment Daemon..."
nohup python3 /Users/silversurfer/Documents/Omniverse2/continuous_seo_deployment_daemon.py > /Users/silversurfer/Documents/Omniverse2/seo_deployment_daemon.log 2>&1 &

echo "Starting 30-Min Keyword Engine..."
nohup python3 /Users/silversurfer/Documents/Omniverse2/seo_30min_keyword_engine.py > /Users/silversurfer/Documents/Omniverse2/seo_keyword_engine.log 2>&1 &

echo "SEO Daemons are now running in the background."
