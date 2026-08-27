# IndexNow setup (5 minutes)

1. Generate a key: `openssl rand -hex 16`
2. Host `https://YOUR_DOMAIN/YOUR_KEY.txt` with the key as file content
3. Ping Bing:

```bash
curl -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json" \
  -d '{"host":"YOUR_DOMAIN","key":"YOUR_KEY","urlList":["https://YOUR_DOMAIN/page.html"]}'
```

4. Add to `seo_engine.py` `indexnow_payload()` and call after each new programmatic page.

Works on gh-pages. Speeds indexing for long-tail SEO pages.
