#!/bin/bash
# ==============================================================================
# LIFT SCHEDULED MAINTENANCE HOLD & RESTORE FULL PRODUCTION WEBSITE
# ==============================================================================
set -e

echo "🔓 Lifting Scheduled Maintenance Hold & Restoring Full Production..."
cp public_html_local/.htaccess.live_backup public_html_local/.htaccess

echo "🚀 Deploying live site restoration to Hostinger..."
./deploy.sh

echo "🎉 Full Production Website is now RESTORED and LIVE on https://www.skyautoservices.com!"
