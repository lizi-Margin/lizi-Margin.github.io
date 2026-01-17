# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AcadHomepage is a Jekyll-based academic personal homepage template with automated Google Scholar citation tracking. It's designed to be forked and customized for individual academic profiles. The project includes:

- Jekyll site with responsive design and SEO optimization
- Automated Google Scholar citation crawler (Python)
- GitHub Actions workflow for scheduled data updates
- SCSS styling with Font Awesome icons

## Development Setup

### Prerequisites
- Ruby with RubyGems
- Bundler (typically included with Ruby)

### Installation
```bash
bundle install
```

### Running Locally
Start the Jekyll development server with live reload:
```bash
bash run_server.sh
```
or directly:
```bash
bundle exec jekyll liveserve
```

The site will be available at `http://127.0.0.1:4000` and will automatically refresh on file changes.

## Key Architecture & Components

### Site Configuration (`_config.yml`)
Central configuration file for the entire site. Key sections:
- **Site metadata**: title, description, repository reference
- **Google Scholar settings**: `google_scholar_stats_use_cdn` (use CDN or raw GitHub for citation data)
- **Author profile**: name, avatar, social links, email, academic profiles
- **Google Analytics**: optional analytics tracking
- **SEO verification**: Google, Bing, Baidu site verification

### Content Structure
- **Homepage content**: `_pages/about.md` - main page displaying publications, news, education, honors, talks, and internships
- **Layouts**: `_layouts/default.html` - single layout used for all pages
- **Includes**: HTML components in `_includes/` including analytics, author profile, masthead, sidebar
- **SCSS styling**: `_sass/` directory organized by component (page, archive, buttons, etc.)

### Google Scholar Integration

The project automatically fetches publication and citation data from Google Scholar:

1. **Data Source**: Python script `google_scholar_crawler/main.py`
   - Uses `scholarly` library to fetch author profile and publications
   - Requires `GOOGLE_SCHOLAR_ID` environment variable (set in GitHub Actions secrets)
   - Outputs two JSON files:
     - `gs_data.json` - full author data including publications
     - `gs_data_shieldsio.json` - citation badge format

2. **GitHub Actions Automation** (`.github/workflows/google_scholar_crawler.yaml`)
   - Triggered: on page build and daily at 08:00 UTC
   - Runs crawler and commits results to `google-scholar-stats` branch
   - Results can be accessed via CDN or raw GitHub URLs

3. **Display in Content**: Use custom Liquid template in `_pages/about.md`:
   ```html
   <span class='show_paper_citations' data='SCHOLAR_PAPER_ID'></span>
   ```
   This displays citation count for individual papers. Paper IDs are found in Google Scholar URLs as `citation_for_view=XXXX`.

### Citation Badge
The citation badge in the homepage (`_pages/about.md`) dynamically displays total citations:
- Uses CDN or raw GitHub URL based on `google_scholar_stats_use_cdn` setting
- Loads from `google-scholar-stats/gs_data_shieldsio.json`
- Renders as a shields.io badge with current citation count

## Common Development Tasks

### Updating Homepage Content
Edit `_pages/about.md` using standard Markdown + HTML. The page uses:
- Markdown for text content
- HTML with CSS classes for structured sections (publications, honors, etc.)
- Special handling for paper citations via `show_paper_citations` spans

### Customizing Site Metadata
Edit `_config.yml`:
- Change title/description at top
- Update author profile section with personal info and social links
- Configure Google Analytics ID if tracking traffic
- Add SEO verification codes

### Adding New Content Sections
Add markdown or HTML directly to `_pages/about.md`. Follow existing patterns (e.g., `# 📝 Publications` uses H1 with emoji).

### Modifying Styling
SCSS files in `_sass/` are compiled to CSS. Key files:
- `_variables.scss` - colors, fonts, spacing
- `_page.scss` - main page layout
- `_sidebar.scss` - author profile sidebar
- `_archive.scss` - list/archive layouts

Changes auto-reload in development via `jekyll liveserve`.

### Running Google Scholar Crawler Locally
To test the citation crawler:
```bash
cd google_scholar_crawler
pip3 install -r requirements.txt
GOOGLE_SCHOLAR_ID=YOUR_ID python3 main.py
```
This generates JSON files in `results/` directory.

## Build & Deployment

### Local Build
Jekyll automatically builds the site in development mode. For production build:
```bash
bundle exec jekyll build
```

The built site goes to `_site/` directory.

### GitHub Pages Deployment
Push changes to the main branch. GitHub Pages automatically builds and deploys using Jekyll. The site is published to `https://USERNAME.github.io` (or your custom domain).

## Important Notes

- **Config Reload**: Changes to `_config.yml` require restarting the Jekyll server
- **Git Branches**: Google Scholar data is committed to the `google-scholar-stats` branch (separate from main)
- **File Inclusion**: Check `_config.yml` `exclude` list - some directories (docs, .github) are excluded from the build
- **Citation Data**: Requires `GOOGLE_SCHOLAR_ID` secret in GitHub repository settings for automation to work
