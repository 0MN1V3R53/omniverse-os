import fs from 'fs';
import path from 'path';

export default function sitemap() {
  const datasetPath = path.join(process.cwd(), 'public', 'assets', 'data', 'cities.json');
  
  // STRICT COMPLIANCE: If the required dataset is missing, we raise an explicit error 
  // rather than hallucinating placeholder values or mock data.
  if (!fs.existsSync(datasetPath)) {
    throw new Error("CRITICAL: Missing dataset for programmatic SEO. Expected public/assets/data/cities.json containing 3000+ location entries. Halting sitemap generation to prevent data hallucination.");
  }
  
  // Existing cities data
  const rawData = fs.readFileSync(datasetPath, 'utf8');
  const cities = JSON.parse(rawData);
  
  const baseUrl = 'https://www.skyautoservices.com';
  
  const cityUrls = cities.map((loc) => ({
    url: `${baseUrl}/auto-transport/${loc.stateSlug}/${loc.citySlug}/`,
    lastModified: new Date(),
    changeFrequency: 'weekly',
    priority: 0.8,
  }));
  
  // Read state-to-state routes data
  const stateRoutesPath = path.join(process.cwd(), 'public', 'assets', 'data', 'state_routes.json');
  let stateRoutesUrls = [];
  let originHubUrls = [];
  
  if (fs.existsSync(stateRoutesPath)) {
    const rawStateRoutes = fs.readFileSync(stateRoutesPath, 'utf8');
    const stateRoutes = JSON.parse(rawStateRoutes);
    
    // Directory Hub
    originHubUrls.push({
      url: `${baseUrl}/state-to-state-routes/`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.9,
    });
    
    for (const [origin, destinations] of Object.entries(stateRoutes)) {
      const originSlug = origin.toLowerCase().replace(/\s+/g, '-');
      
      // Origin Hub Pages
      originHubUrls.push({
        url: `${baseUrl}/state-to-state-routes/${originSlug}/`,
        lastModified: new Date(),
        changeFrequency: 'weekly',
        priority: 0.8,
      });
      
      // Final Static Route Pages
      for (const route of destinations) {
        stateRoutesUrls.push({
          url: `${baseUrl}/routes/${route.slug}`,
          lastModified: new Date(),
          changeFrequency: 'monthly',
          priority: 0.7,
        });
      }
    }
  }
  
  return [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1.0,
    },
    ...cityUrls,
    ...originHubUrls,
    ...stateRoutesUrls
  ];
}
