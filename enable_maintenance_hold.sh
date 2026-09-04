#!/bin/bash
# ==============================================================================
# ENABLE SCHEDULED MAINTENANCE & MARKETING INITIALIZATION HOLD
# ==============================================================================
set -e

echo "🔒 Activating Scheduled Maintenance / Marketing Initialization Hold..."
cp public_html_local/.htaccess.maintenance public_html_local/.htaccess 2>/dev/null || true

echo "🚀 Deploying maintenance hold to Hostinger..."
./deploy.sh

echo "✅ Scheduled Maintenance Hold is LIVE on https://www.skyautoservices.com!"
