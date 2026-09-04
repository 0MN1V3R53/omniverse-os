const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const OUT_DIR = path.resolve(__dirname, '../out');
const PORT = 3009;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.ttf': 'font/ttf',
};

function createStaticServer() {
  return http.createServer((req, res) => {
    let reqPath = req.url.split('?')[0];
    if (reqPath === '/') reqPath = '/index.html';
    
    let filePath = path.join(OUT_DIR, reqPath);

    // If directory or no ext, check .html or /index.html
    if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
      if (fs.existsSync(filePath + '.html')) {
        filePath = filePath + '.html';
      } else if (fs.existsSync(path.join(filePath, 'index.html'))) {
        filePath = path.join(filePath, 'index.html');
      }
    }

    if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
      const ext = path.extname(filePath).toLowerCase();
      res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'application/octet-stream' });
      fs.createReadStream(filePath).pipe(res);
    } else {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
    }
  });
}

const VIEWPORTS = [
  { name: 'iPhone SE', width: 320, height: 568 },
  { name: 'iPhone mini', width: 375, height: 667 },
  { name: 'iPhone 14', width: 390, height: 844 },
  { name: 'iPhone 14 Pro Max', width: 430, height: 932 },
  { name: 'iPad mini', width: 768, height: 1024 },
  { name: 'iPad Pro / Laptop', width: 1024, height: 768 },
  { name: 'Desktop', width: 1280, height: 800 },
  { name: 'FHD Desktop', width: 1920, height: 1080 },
  { name: '4K Ultrawide', width: 2560, height: 1440 },
];

const PAGES = [
  '/',
  '/services',
  '/about',
  '/contact',
  '/privacy',
  '/terms',
  '/routes',
  '/routes-directory',
  '/state-to-state-routes',
  '/state-to-state-routes/california',
  '/routes/alabama-to-arizona-auto-transport',
  '/auto-transport/illinois/chicago',
  '/usa-auto-transport-news',
  '/usa-auto-transport-news/2026-snowbird-auto-transport-season-predictions'
];

async function main() {
  console.log('🚀 Starting Embedded Static File Server for Multi-Viewport Ergonomic Audit...');
  const server = createStaticServer();

  await new Promise((resolve) => {
    server.listen(PORT, '127.0.0.1', () => {
      console.log(`✅ Static Server running on http://127.0.0.1:${PORT}`);
      resolve();
    });
  });

  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  let totalTests = 0;
  let passedTests = 0;
  const issues = [];

  for (const pagePath of PAGES) {
    const url = `http://127.0.0.1:${PORT}${pagePath}`;
    console.log(`\n📄 Auditing Route: ${pagePath}`);

    for (const vp of VIEWPORTS) {
      totalTests++;
      const context = await browser.newContext({
        viewport: { width: vp.width, height: vp.height },
      });
      const page = await context.newPage();

      try {
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 });
        
        // Evaluate ergonomic constraints
        const metrics = await page.evaluate(() => {
          const navElements = document.querySelectorAll('nav');
          const body = document.body;
          const html = document.documentElement;
          const scrollWidth = Math.max(body.scrollWidth, html.scrollWidth);
          const clientWidth = window.innerWidth;
          const hasHorizontalOverflow = scrollWidth > clientWidth + 1; // 1px tolerance

          // Check if h1 or main content is occluded by fixed header
          const h1 = document.querySelector('h1');
          let h1Occluded = false;
          let h1Top = null;
          let navBottom = null;

          if (h1 && navElements.length > 0) {
            const h1Rect = h1.getBoundingClientRect();
            const navRect = navElements[0].getBoundingClientRect();
            h1Top = h1Rect.top;
            navBottom = navRect.bottom;
            // If nav covers h1 top
            if (navRect.bottom > h1Rect.top && h1Rect.bottom > navRect.top) {
              h1Occluded = true;
            }
          }

          return {
            navCount: navElements.length,
            hasHorizontalOverflow,
            scrollWidth,
            clientWidth,
            h1Occluded,
            h1Top,
            navBottom,
          };
        });

        let testPassed = true;
        const testErrors = [];

        if (metrics.navCount !== 1) {
          testPassed = false;
          testErrors.push(`Expected exactly 1 <nav>, found ${metrics.navCount}`);
        }
        if (metrics.hasHorizontalOverflow) {
          testPassed = false;
          testErrors.push(`Horizontal overflow detected: scrollWidth=${metrics.scrollWidth} > clientWidth=${metrics.clientWidth}`);
        }
        if (metrics.h1Occluded) {
          testPassed = false;
          testErrors.push(`H1 occluded by navbar: h1Top=${metrics.h1Top} <= navBottom=${metrics.navBottom}`);
        }

        if (testPassed) {
          passedTests++;
          process.stdout.write(`  [${vp.name} (${vp.width}px)] ✓ PASS\n`);
        } else {
          process.stdout.write(`  [${vp.name} (${vp.width}px)] ✗ FAIL: ${testErrors.join(', ')}\n`);
          issues.push({
            page: pagePath,
            viewport: vp.name,
            width: vp.width,
            errors: testErrors,
          });
        }
      } catch (err) {
        issues.push({
          page: pagePath,
          viewport: vp.name,
          width: vp.width,
          errors: [err.message],
        });
        process.stdout.write(`  [${vp.name} (${vp.width}px)] ✗ ERROR: ${err.message}\n`);
      } finally {
        await context.close();
      }
    }
  }

  await browser.close();
  server.close();

  console.log('\n========================================');
  console.log(`AUDIT RESULTS: ${passedTests} / ${totalTests} Viewport Tests Passed (${((passedTests / totalTests) * 100).toFixed(1)}%)`);
  console.log('========================================');

  if (issues.length === 0) {
    console.log('🎉 100% PERFECT RESPONSIVENESS AND ERGONOMICS ACROSS ALL TESTED VIEWPORTS!');
    process.exit(0);
  } else {
    console.error(`⚠️ Found ${issues.length} ergonomic issues.`);
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
