const http = require('http');
const { chromium } = require('playwright');
const { spawn } = require('child_process');

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
  '/routes/california-to-florida-auto-transport',
  '/auto-transport/california/los-angeles',
  '/usa-auto-transport-news',
  '/usa-auto-transport-news/2026-snowbird-auto-transport-season-predictions'
];

async function main() {
  console.log('🚀 Starting Next.js Production Server for Multi-Viewport Ergonomic Audit...');
  const nextServer = spawn('npx', ['next', 'start', '-p', '3009'], {
    cwd: __dirname + '/../montway_clone',
    stdio: 'pipe',
  });

  // Wait for server to become responsive
  await new Promise((resolve, reject) => {
    let attempts = 0;
    const interval = setInterval(() => {
      attempts++;
      http.get('http://127.0.0.1:3009/', (res) => {
        if (res.statusCode === 200) {
          clearInterval(interval);
          resolve();
        }
      }).on('error', () => {
        if (attempts > 30) {
          clearInterval(interval);
          reject(new Error('Server failed to start in 30s'));
        }
      });
    }, 1000);
  });

  console.log('✅ Server ready on http://127.0.0.1:3009');
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  let totalTests = 0;
  let passedTests = 0;
  const issues = [];

  for (const pagePath of PAGES) {
    const url = `http://127.0.0.1:3009${pagePath}`;
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
          const hasHorizontalOverflow = scrollWidth > clientWidth;

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
            // If nav is fixed/sticky and covers h1 top
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
  nextServer.kill();

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
