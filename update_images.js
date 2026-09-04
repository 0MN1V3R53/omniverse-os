const fs = require('fs');

const images = [
  "https://images.unsplash.com/photo-1626121300305-def4dc305387?w=1200&q=80",
  "https://images.unsplash.com/photo-1761917904658-2a9ecb84a169?w=1200&q=80",
  "https://images.unsplash.com/photo-1686246668933-7425658394b0?w=1200&q=80",
  "https://images.unsplash.com/photo-1651884533118-cc8e1a8b35e5?w=1200&q=80",
  "https://images.unsplash.com/photo-1761133381018-aed5063d22fe?w=1200&q=80",
  "https://images.unsplash.com/photo-1774116196662-a9e1e4fa1612?w=1200&q=80",
  "https://images.unsplash.com/photo-1766785368863-f2188a8c8b32?w=1200&q=80"
];

const filePath = 'montway_clone/public/data/news_articles.json';
const data = fs.readFileSync(filePath, 'utf8');
const articles = JSON.parse(data);

articles.forEach((article, index) => {
  article.backgroundImage = images[index % images.length];
});

fs.writeFileSync(filePath, JSON.stringify(articles, null, 2), 'utf8');
console.log('Updated all article images successfully.');
