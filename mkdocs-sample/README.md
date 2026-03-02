# MkDocs with GC Design System (GCDS) Theme

Custom MkDocs theme implementing Government of Canada Design System (GCDS) Web Components with WCAG 2.1 AA compliance.

> **Project Note**: This site was built fresh with GCDS theme. The `docs/MIGRATION.md` file is a reference guide for teams who need to migrate existing Material for MkDocs sites to GCDS - no actual migration occurred in this project.

## Features

- ✅ Full GCDS Web Components integration
- ✅ Canada.ca contextual alert styling
- ✅ Collapsible admonitions with keyboard navigation
- ✅ Bilingual support (EN/FR toggle)
- ✅ WCAG 2.1 AA accessibility
- ✅ No Material theme dependency

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm

## Quick Start

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install GCDS Components

```bash
npm install
```

This installs `@cdssnc/gcds-components@0.47.0` and copies assets to `docs/assets/gcds/`.

### 3. Build Site

```bash
python -m mkdocs build
```

### 4. Serve Locally

```bash
python -m mkdocs serve
```

Visit: http://127.0.0.1:8000

## Validation

```bash
python scripts/quick_validation.py
```

Expected output: `OVERALL: PASS` with all file checks passing.

## Troubleshooting

### Missing GCDS Assets Error

**Symptom**: Validation shows `site/assets/gcds/gcds.css` missing

**Fix**:
```bash
# Verify npm installed correctly
npm install

# Check assets copied
ls docs/assets/gcds/

# If empty, manually copy
node copy-gcds-assets.js

# Rebuild
python -m mkdocs build --clean

# Revalidate
python scripts/quick_validation.py
```

### Build Errors

**Template not found**: Verify `gcds-theme/` contains base.html, main.html, and partials/

**Import errors**: Run `pip install -r requirements.txt`

## Project Structure

```
mkdocs-sample/
├── gcds-theme/              # Custom Jinja2 templates
│   ├── base.html
│   ├── main.html
│   └── partials/
├── docs/                    # Documentation content
│   ├── assets/gcds/         # GCDS components (from npm)
│   ├── stylesheets/
│   ├── javascripts/
│   └── fr/
├── scripts/
│   ├── validate_gcds_theme.py
│   └── quick_validation.py
├── mkdocs.yml
├── package.json
└── requirements.txt
```

## Deployment

### Azure Static Website

```bash
python -m mkdocs build --clean
# Upload site/ to Azure Blob Storage $web container
```

### SharePoint Online

```bash
python -m mkdocs build --clean
# Upload site/ to SharePoint document library
# Note: CSP may block Web Components
```

## Documentation

- **Implementation Patterns**: [docs/MIGRATION.md](docs/MIGRATION.md) - Reference guide comparing Material to GCDS (useful for teams migrating existing sites)
- **GC Design System**: https://design-system.alpha.canada.ca/
- **MkDocs**: https://www.mkdocs.org/

## Version

- **MkDocs**: 1.5+
- **GCDS Components**: 0.47.0
- **Python**: 3.10+
- **Node.js**: 18+
