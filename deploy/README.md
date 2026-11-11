# Releasing to supplementsbyhazel.com

The live site runs on Wix hosting as this Astro project (from Wix Go Headless, completed 11 Nov 2026).

1. `python3 build.py` (repo root), then copy `public/` into `deploy/public/`.
2. In `deploy/`: `npm install`, then `WIX_CLIENT_ID=d8aa01b1-df88-486f-a073-8ffc438cf7c6 npx astro build`.
3. Zip the build (`dist/` and `.wix/` with the project) and release it with the Wix MCP tool
   `UploadHeadlessWebsiteFiles` to site `f5b3a5e6-81ea-4219-a1bc-631868be13b4` (prepare, PUT, release).

`src/pages/index.astro` and `404.astro` serve the static pages; every other `.astro` file is a 301
from an old Wix address (see `redirects.json`).
