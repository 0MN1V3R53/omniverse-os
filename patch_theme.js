const fs = require('fs');
const path = require('path');

const walkSync = (dir, filelist = []) => {
  fs.readdirSync(dir).forEach(file => {
    const dirFile = path.join(dir, file);
    try { filelist = walkSync(dirFile, filelist); }
    catch (err) {
      if (err.code === 'ENOTDIR' || err.code === 'EBADF') {
        if (dirFile.endsWith('page.js') || dirFile.endsWith('layout.js')) {
          filelist.push(dirFile);
        }
      }
    }
  });
  return filelist;
};

const files = walkSync('/Users/silversurfer/Documents/Omniverse2/montway_clone/app');

files.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  let original = content;

  // Replace layout.js specific dark mode
  if (file.endsWith('layout.js')) {
    content = content.replace('className="dark"', '');
    content = content.replace('bg-black text-white', 'bg-white text-slate-900');
  } else {
    // Replace dark mode classes in page.js
    content = content.replace(/bg-black/g, 'bg-white');
    content = content.replace(/text-white/g, 'text-slate-900');
    content = content.replace(/text-gray-400/g, 'text-slate-600');
    content = content.replace(/text-gray-300/g, 'text-slate-700');
    content = content.replace(/bg-zinc-950/g, 'bg-slate-50');
    content = content.replace(/bg-zinc-900/g, 'bg-white');
    content = content.replace(/border-white\/10/g, 'border-slate-200');
    content = content.replace(/border-white\/5/g, 'border-slate-100');
    content = content.replace(/bg-black\/50/g, 'bg-slate-100');
    content = content.replace(/bg-black\/40/g, 'bg-slate-100');
    content = content.replace(/bg-black\/60/g, 'bg-slate-900/60');
    
    // Add marketing sections to the bottom of the page if not present
    if (file.indexOf('app/page.js') === -1) {
      if (content.indexOf('MontwayMarketingSections') === -1) {
        // Need to add import
        content = `import MontwayMarketingSections from '@/components/MontwayMarketingSections';\n` + content;
        
        // Need to add component before </main>
        content = content.replace('</main>', '  <MontwayMarketingSections />\n    </main>');
      }
      
      // Ensure QuoteCalculatorWrapper is present
      if (content.indexOf('QuoteCalculatorWrapper') === -1) {
        content = `import QuoteCalculatorWrapper from '@/components/QuoteCalculatorWrapper';\n` + content;
        content = content.replace('<MontwayMarketingSections />', '<QuoteCalculatorWrapper />\n        <MontwayMarketingSections />');
      }
    }
  }

  if (content !== original) {
    fs.writeFileSync(file, content);
    console.log('Updated:', file);
  }
});
