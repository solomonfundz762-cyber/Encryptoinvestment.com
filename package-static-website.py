import os
import shutil
import zipfile

def package_static_website():
    workspace_root = os.path.abspath(os.getcwd())
    dist_dir = os.path.join(workspace_root, 'dist')
    dist_assets = os.path.join(dist_dir, 'assets')
    dist_index = os.path.join(dist_dir, 'index.html')

    if not os.path.exists(dist_index):
        print("dist/index.html not found! Please build the project first.")
        return

    output_dir = os.path.join(workspace_root, 'static-website')
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # 1. Copy the main production homepage (index.html)
    shutil.copy2(dist_index, os.path.join(output_dir, 'index.html'))

    # 2. Copy the production assets directory
    target_assets_dir = os.path.join(output_dir, 'assets')
    if os.path.exists(dist_assets):
        shutil.copytree(dist_assets, target_assets_dir)

    # 3. Create 404.html (GitHub Pages SPA fallback so deep links and refreshing work)
    shutil.copy2(dist_index, os.path.join(output_dir, '404.html'))

    # 4. Create .nojekyll (tells GitHub Pages to disable Jekyll processing)
    nojekyll_path = os.path.join(output_dir, '.nojekyll')
    with open(nojekyll_path, 'w') as f:
        f.write('# Disable Jekyll on GitHub Pages\n')

    # 5. Copy companion multi-page static HTML files, style.css, script.js
    companion_files = [
        'about.html',
        'admin.html',
        'contact.html',
        'dashboard.html',
        'features.html',
        'how-to-invest.html',
        'investment-plans.html',
        'legal.html',
        'login.html',
        'market-rates.html',
        'register.html',
        'style.css',
        'script.js'
    ]

    for fname in companion_files:
        src_path = os.path.join(workspace_root, fname)
        if os.path.exists(src_path):
            shutil.copy2(src_path, os.path.join(output_dir, fname))

    # Also copy manifest.json from public if present
    public_manifest = os.path.join(workspace_root, 'public', 'manifest.json')
    if os.path.exists(public_manifest):
        shutil.copy2(public_manifest, os.path.join(output_dir, 'manifest.json'))

    # 6. Create README.md inside static-website with clear GitHub Pages deployment instructions
    readme_content = """# Encrypto Investment - Production Static Website Package

This folder contains the complete, production-ready static website package, configured with **relative asset paths** (`./assets/...`) for seamless hosting on **GitHub Pages**, **Netlify**, **Vercel**, **Cloudflare Pages**, or any static web hosting provider.

---

## Which file is the main homepage?

> **`index.html`** is the main homepage and primary application entry point.
> When you open `index.html` in any modern web browser or deploy it to GitHub Pages, the entire platform loads instantly with all interactive features, real-time rates, wallet dashboards, investment plans, and investor relations.

---

## Directory Structure

```
static-website/
├── index.html        <-- MAIN HOMEPAGE (Starts the entire React app with relative paths)
├── 404.html          <-- GitHub Pages fallback (prevents 404 errors on page refresh)
├── .nojekyll         <-- GitHub Pages configuration (bypasses Jekyll processing)
├── assets/           <-- Production JavaScript, CSS, and media bundles
│   ├── index-*.js    <-- Compiled application logic and UI components
│   ├── index-*.css   <-- Complete Tailwind CSS and typography styling
│   └── *.jpg         <-- Optimized images and media
├── about.html        <-- Corporate overview & leadership page
├── admin.html        <-- Administrative compliance console
├── contact.html      <-- Institutional client desk
├── dashboard.html    <-- Standalone client dashboard
├── features.html     <-- Security and vault features
├── how-to-invest.html<-- Onboarding guide
├── investment-plans.html<-- Staking & investment plans
├── legal.html        <-- Terms of service & risk disclosures
├── login.html        <-- Authentication gateway
├── market-rates.html <-- Live cryptocurrency rates
├── register.html     <-- Account registration page
├── style.css         <-- Companion stylesheet
├── script.js         <-- Companion helper script
└── manifest.json     <-- Web App Manifest
```

---

## How to Deploy to GitHub Pages (Step-by-Step)

### Method A: Uploading via GitHub Web Interface (Easiest, No Git Command Line Required)

1. **Create a new GitHub Repository**:
   - Go to [github.com/new](https://github.com/new)
   - Name your repository (e.g. `encrypto-invest` or `username.github.io`)
   - Select **Public**, leave "Initialize with README" unchecked, and click **Create repository**.

2. **Upload the Files**:
   - On your new repository page, click **uploading an existing file**.
   - Drag and drop **all files and the `assets/` folder** from this folder directly into the GitHub web uploader.
   - Ensure `index.html` is in the repository's **root directory** (not inside a subfolder).
   - Click **Commit changes**.

3. **Enable GitHub Pages**:
   - In your repository, click the **Settings** tab.
   - In the left sidebar, click **Pages**.
   - Under **Build and deployment > Source**, select **Deploy from a branch**.
   - Under **Branch**, select `main` (or `master`) and folder `/ (root)`.
   - Click **Save**.
   - Within 1–2 minutes, GitHub will display your live site URL:
     `https://<your-username>.github.io/<repository-name>/`

---

### Method B: Using Git Command Line

```bash
cd static-website
git init
git add .
git commit -m "Deploy Encrypto Investment static website"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main --force
```

Then go to **Repository Settings > Pages**, select `main` branch `/ (root)`, and save.

---

## Relative Paths Verification

All asset references in `index.html` and companion pages are strictly relative (`./assets/...`), ensuring that the website functions whether hosted at:
- A custom domain (`https://www.yourdomain.com/`)
- A GitHub Pages root domain (`https://<username>.github.io/`)
- A GitHub Pages repository subpath (`https://<username>.github.io/<repo-name>/`)
- An offline local folder (`file:///...`)
"""
    with open(os.path.join(output_dir, 'README.md'), 'w') as f:
        f.write(readme_content)

    # 7. Create static-website.zip archive
    zip_filename = "static-website.zip"
    public_zip = os.path.join(workspace_root, "public", zip_filename)
    root_zip = os.path.join(workspace_root, zip_filename)
    dist_zip = os.path.join(dist_dir, zip_filename)

    with zipfile.ZipFile(public_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in sorted(files):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, output_dir)
                zipf.write(full_path, rel_path)

    # Copy to root and dist
    shutil.copy2(public_zip, root_zip)
    shutil.copy2(public_zip, dist_zip)

    size_mb = os.path.getsize(public_zip) / (1024 * 1024)
    print(f"Successfully packaged static website into '{zip_filename}' ({size_mb:.2f} MB)")
    print(f"Directory: {output_dir}")
    print(f"Archives saved at:\n - {public_zip}\n - {root_zip}\n - {dist_zip}")

if __name__ == '__main__':
    package_static_website()
