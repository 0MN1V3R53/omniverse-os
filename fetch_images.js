const fs = require('fs');
const { execSync } = require('child_process');

// Read the existing JSON
const filePath = 'montway_clone/public/data/news_articles.json';
const articles = JSON.parse(fs.readFileSync(filePath, 'utf8'));

console.log("Scraping Unsplash using curl...");
const queries = [
  "semi-truck-highway", 
  "car-carrier-truck", 
  "auto-transport", 
  "highway-logistics", 
  "muscle-car-highway",
  "classic-car-driving",
  "logistics",
  "shipping-port",
  "truck-driving"
];
const uniqueIds = new Set();

for (const q of queries) {
  try {
    const html = execSync(`curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "https://unsplash.com/s/photos/${q}"`).toString();
    const matches = html.match(/https:\/\/images\.unsplash\.com\/photo-[a-zA-Z0-9\-]+/g);
    if (matches) {
      matches.forEach(m => {
        const id = m.split('photo-')[1].split('?')[0];
        uniqueIds.add(id);
      });
    }
  } catch (e) {
    console.error("Error scraping", q);
  }
}

const idArray = Array.from(uniqueIds);
console.log(`Found ${idArray.length} unique images. Assigning to articles...`);

for (let i = 0; i < articles.length; i++) {
  const photoId = idArray[i] || idArray[i % idArray.length] || "1626121300305-def4dc305387"; 
  articles[i].backgroundImage = `https://images.unsplash.com/photo-${photoId}?w=1200&q=80`;
}

fs.writeFileSync(filePath, JSON.stringify(articles, null, 2), 'utf8');
console.log(`Successfully assigned unique images to ${articles.length} articles.`);
