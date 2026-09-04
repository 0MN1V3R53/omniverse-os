const fs = require('fs');

const keywords = [
  "semi,highway", "mustang,highway", "car,transport", "truck,driving",
  "logistics,highway", "corvette,road", "freightliner,truck", "camaro,highway",
  "highway,traffic", "kenworth,truck", "peterbilt,highway", "sports,car,road",
  "truck,interstate", "shipping,logistics", "auto,carrier", "highway,sunset",
  "muscle,car", "usa,highway,truck", "freeway,traffic", "transport,truck",
  "dodge,challenger", "cargo,ship,port", "snow,driving", "container,truck",
  "flatbed,tow,truck"
];

const filePath = 'montway_clone/public/data/news_articles.json';
const articles = JSON.parse(fs.readFileSync(filePath, 'utf8'));

for (let i = 0; i < articles.length; i++) {
  const kw = keywords[i % keywords.length];
  articles[i].backgroundImage = `https://loremflickr.com/1200/800/${kw}/all?lock=${i + 1}`;
}

fs.writeFileSync(filePath, JSON.stringify(articles, null, 2), 'utf8');
console.log("Assigned 25 bespoke LoremFlickr images to articles.");
