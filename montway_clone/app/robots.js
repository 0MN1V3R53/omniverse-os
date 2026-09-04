export default function robots() {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin', '/api'],
      },
      {
        userAgent: ['GPTBot', 'Claude-Web', 'Google-Extended', 'KimiBot'],
        allow: ['/', '/llm-feed.json'],
      }
    ],
    sitemap: 'https://www.skyautoservices.com/sitemap.xml',
  }
}
