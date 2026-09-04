# HOSTINGER DEPLOYMENT & TROUBLESHOOTING GUIDE: AETHER CORE 999
**Document Code:** `ethercore999666`  
**Target Domain:** `apolloleads.info`  
**Target Platform:** Hostinger Web Hosting (hPanel / LiteSpeed / Apache)  
**Project:** Aether Core Digital Archive (`index.html`, `assets/`, `docs/`, `.htaccess`)

---

## 🚨 CRITICAL DIAGNOSIS: Why `apolloleads.info` is Throwing 404s

When we ran direct network diagnostics on `https://apolloleads.info`, the server returned:
```text
HTTP/2 200
server: hcdn
x-powered-by: Hostinger Horizons
<title>Apollo Leads</title>
<script type="module" crossorigin src="/assets/index-nK2Zbmp7.js"></script>
<link rel="stylesheet" crossorigin href="/assets/index-B5DLRsUD.css">
```

### The Root Cause:
Your domain `apolloleads.info` is currently assigned to **Hostinger Horizons (Hostinger AI Website Builder)** instead of **Hostinger Web Hosting (File Manager)**.

- **Hostinger Horizons** is a separate cloud builder platform running on Hostinger's CDN (`hcdn`).
- It is serving an old, broken "Apollo Leads" template from June 2026 that is trying to load `/assets/index-nK2Zbmp7.js` (which does not exist, causing the 404).
- **As long as the domain is attached to Horizons, Hostinger completely ignores your File Manager and `public_html` folder.**

---

## 🛠️ THE EXACT FIX: How to Connect `apolloleads.info` to Web Hosting (File Manager)

Follow these exact steps in your Hostinger control panel (**hPanel**):

### Step 1: Disconnect `apolloleads.info` from Hostinger Horizons / AI Builder
1. Log in to your **Hostinger Account** at [https://hpanel.hostinger.com](https://hpanel.hostinger.com).
2. Click on **Websites** in the top navigation bar.
3. Find `apolloleads.info`. You will notice it says **AI Builder** or **Horizons**.
4. Click the **three dots menu (⋯)** next to `apolloleads.info` $\rightarrow$ click **Delete** (or **Change Platform**).
   *(This frees `apolloleads.info` from the broken Horizons cloud container).*

---

### Step 2: Add `apolloleads.info` as a Standard Web Hosting Site
1. Still inside the **Websites** tab, click the purple button: **+ Add Website** (or **Create/Migrate Website**).
2. When asked *"What type of website do you want to create?"*:
   - Click **Skip, create a blank website** (or select **Other / Custom HTML**).
   - **DO NOT** select "Hostinger AI Builder" or "Horizons".
3. When asked for your domain:
   - Select **Use an Existing Domain** $\rightarrow$ enter `apolloleads.info`.
   - Complete the setup.

---

### Step 3: Upload the Fresh Website Files via File Manager
Now that `apolloleads.info` is connected to standard web hosting, `public_html` is active!

1. In hPanel $\rightarrow$ **Websites** $\rightarrow$ click **Manage** next to `apolloleads.info`.
2. In the sidebar, click **File Manager** $\rightarrow$ double-click to open **`public_html`**.
3. **Delete any placeholder files** (like `default.php`).
4. Click the **Upload** icon ($\uparrow$) $\rightarrow$ upload:
   `/Users/silversurfer/Documents/aether Core 999/aether-core-website.zip`
5. Right-click `aether-core-website.zip` $\rightarrow$ click **Extract** $\rightarrow$ set target folder to **`.`** (dot) or `/public_html`.
6. Delete the `.zip` file after extracting.

---

### Step 4: Verify the Files in `public_html`
Confirm that inside `public_html` you see:
- [x] `index.html` (Points to `index-FI1nEeFu.js` and `index-CBmQf2J_.css`)
- [x] `.htaccess`
- [x] `assets/`
  - `index-CBmQf2J_.css`
  - `index-FI1nEeFu.js`
- [x] `docs/` (containing `manifest.json` and `doc_1.md` to `doc_49.md`)
- [x] `sigil.png`, `goetia_sigils.png`, `icons.svg`, `favicon.svg`

---

### Step 5: Test the Live Domain
1. Open an **Incognito / Private Window** in your browser.
2. Visit [https://apolloleads.info](https://apolloleads.info).
3. The 404 error will be gone, and the full 3D Aether Core interactive archive will load immediately.

---
*Created for Aether Core 999 Archive Project. Reference: `ethercore999666`.*
