#!/bin/bash
rsync -av --delete --exclude="api" --exclude="assets" montway_clone/out/ public_html_local/

# Fix Next.js static export missing index.html for directory routes
for dir in public_html_local/*/; do
  dir_name=$(basename "$dir")
  if [ -f "public_html_local/${dir_name}.html" ]; then
    cp "public_html_local/${dir_name}.html" "${dir}index.html"
  fi
done

# Generate .htaccess to fix trailing slash 500 errors, enforce canonical redirects, HSTS, compression, caching, and custom 404
cat << 'EOF' > public_html_local/.htaccess
Options -MultiViews
RewriteEngine On

# 1. Canonical Redirect: Force HTTPS and WWW (https://www.skyautoservices.com)
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} ^skyautoservices\.com$ [NC]
RewriteRule ^(.*)$ https://www.skyautoservices.com/$1 [L,R=301]

# 2. Redirect trailing slash to non-trailing slash if not a directory
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)/$ /$1 [L,R=301]

# 3. Append .html if the file exists
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME}\.html -f
RewriteRule ^(.*)$ $1.html [L]

# 4. Custom 404 Error Document
ErrorDocument 404 /404.html

# 5. Anti-Scraping & Site Ripper Defense (Blocks automated dumpers, offline rippers, and data-mining harvesters)
RewriteCond %{HTTP_USER_AGENT} (HTTrack|Wget|Scrapy|Python-urllib|libwww-perl|Go-http-client|Teleport|WebCopier|Offline\ Explorer|SiteSnagger|EmailCollector|AutoHTTP|WebBandit|WebSauger|WebReaper|SiteSucker) [NC]
RewriteRule .* - [F,L]

# 6. Security Headers (HSTS, MIME-sniffing, Framing, Referrer, Permissions, XSS Protection)
<IfModule mod_headers.c>
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(self)"
</IfModule>


# 6. Gzip / Deflate Compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript
    AddOutputFilterByType DEFLATE application/xml application/xhtml+xml application/rss+xml
    AddOutputFilterByType DEFLATE application/javascript application/x-javascript application/json
    AddOutputFilterByType DEFLATE image/svg+xml
</IfModule>

# 7. Browser Caching & Expires Headers
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType text/html "access plus 1 hour"
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/webp "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
    ExpiresByType image/x-icon "access plus 1 year"
    ExpiresByType font/woff2 "access plus 1 year"
    ExpiresByType font/woff "access plus 1 year"
    ExpiresByType application/font-woff2 "access plus 1 year"
</IfModule>

<IfModule mod_headers.c>
    <FilesMatch "\.(ico|jpe?g|png|gif|webp|svg|woff2?|ttf|otf|css|js)$">
        Header set Cache-Control "max-age=31536000, public, immutable"
    </FilesMatch>
    <FilesMatch "\.(html|json)$">
        Header set Cache-Control "max-age=3600, public, must-revalidate"
    </FilesMatch>
</IfModule>
EOF

./deploy.sh

