const fs = require('fs');
const https = require('https');

// Queries that will yield modern American cars and trucks
const queries = [
  "Ford Mustang GT 2020",
  "Chevrolet Corvette C8",
  "Dodge Challenger SRT Hellcat",
  "Tesla Model S on road",
  "Ford F-150 Raptor",
  "Freightliner Cascadia",
  "Kenworth T680",
  "Peterbilt 579",
  "Volvo VNL truck",
  "American highway traffic",
  "Chevrolet Camaro ZL1",
  "Dodge Charger SRT",
  "Ford Mustang Mach-E",
  "Rivian R1T",
  "GMC Hummer EV",
  "Tesla Semi truck",
  "Interstate Highway USA",
  "Florida highway traffic",
  "Texas highway traffic",
  "Car carrier trailer modern",
  "Auto transport truck USA",
  "Roll-on/roll-off ship",
  "Port of Long Beach cargo",
  "Port of Seattle cargo",
  "Winter driving USA highway"
];

const uniqueUrls = [];

function fetchWikiImage(query) {
  return new Promise((resolve) => {
    const url = `https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages|imageinfo&generator=search&gsrsearch=${encodeURIComponent(query)}&gsrnamespace=0|6&gsrlimit=3&iiprop=url&piprop=original`;
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.query && json.query.pages) {
            for (let pageId in json.query.pages) {
              const page = json.query.pages[pageId];
              let imgUrl = null;
              if (page.original && page.original.source) {
                 imgUrl = page.original.source;
              } else if (page.imageinfo && page.imageinfo[0] && page.imageinfo[0].url) {
                 imgUrl = page.imageinfo[0].url;
              }
              
              if (imgUrl && !imgUrl.endsWith('.svg') && !imgUrl.endsWith('.pdf')) {
                uniqueUrls.push(imgUrl);
                return resolve();
              }
            }
          }
          resolve();
        } catch(e) {
          resolve();
        }
      });
    }).on('error', () => resolve());
  });
}

async function run() {
  for (const q of queries) {
    await fetchWikiImage(q);
  }
  
  const filePath = 'montway_clone/public/data/news_articles.json';
  const articles = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  
  for (let i = 0; i < articles.length; i++) {
    const img = uniqueUrls[i] || uniqueUrls[i % uniqueUrls.length] || "https://upload.wikimedia.org/wikipedia/commons/e/e8/I-805_San_Diego_Skyline.jpg";
    articles[i].backgroundImage = img;
  }
  
  fs.writeFileSync(filePath, JSON.stringify(articles, null, 2), 'utf8');
  console.log(`Assigned ${uniqueUrls.length} unique Wikipedia images to 25 articles.`);
}

run();
