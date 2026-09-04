#!/bin/bash
# Incremental Deployment Script (syncs only updated files)

echo "🚀 Syncing changed files incrementally to Hostinger domain root..."
rsync -avz --delete --exclude='.DS_Store' --exclude='.well-known' --exclude='cgi-bin' --include='/data/*.json' --exclude='*.json' --exclude='venv' -e "ssh -p 65002 -i ~/.ssh/id_ed25519" public_html_local/ u803913036@82.198.228.154:domains/skyautoservices.com/public_html/
rsync -avz --delete --exclude='.DS_Store' --exclude='.well-known' --exclude='cgi-bin' --include='/data/*.json' --exclude='*.json' --exclude='venv' -e "ssh -p 65002 -i ~/.ssh/id_ed25519" public_html_local/ u803913036@82.198.228.154:public_html/

echo "⚡ Clearing Hostinger LiteSpeed & Edge cache..."
ssh -p 65002 -i ~/.ssh/id_ed25519 u803913036@82.198.228.154 "cd domains/skyautoservices.com/public_html && touch .litespeed_purge && rm -f .litespeed_purge"
ssh -p 65002 -i ~/.ssh/id_ed25519 u803913036@82.198.228.154 "cd public_html && touch .litespeed_purge && rm -f .litespeed_purge"
curl -s -X PURGE https://skyautoservices.com/ > /dev/null
curl -s -X PURGE https://www.skyautoservices.com/ > /dev/null

echo "✅ Incremental update complete! Only changed files were uploaded."

