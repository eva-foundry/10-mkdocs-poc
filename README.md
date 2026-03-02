# Project 10: MkDocs Proof of Concept

**Project Status**: Active - Implementation Phase  
**Start Date**: January 24, 2026  
**Owner**: Marco Presta  
**Type**: Documentation Infrastructure PoC

---

## Executive Summary

This project validates MkDocs as a static site generator for EVA documentation with two critical hosting tests:
1. **SharePoint Online** (document library) - Test if static HTML renders or forces download
2. **Azure Static Website** - Validate reliable static hosting for production docs

**Success Criteria**: Determine optimal hosting strategy for EVA documentation ecosystem.

---

## Goals

### Primary Objectives
1. ✅ Generate professional MkDocs site with **real EVA production assets** (103 assets: 93 visual + 10 library docs)
2. ⏳ Test SharePoint Online static HTML rendering capabilities
3. ⏳ Validate Azure Static Website hosting (baseline)
4. ⏳ Document findings and recommend hosting strategy

### Secondary Objectives
5. ✅ Establish MkDocs best practices for EVA ecosystem
6. ✅ Create reusable MkDocs templates for future projects
7. ⏳ Test deep linking, navigation, and asset loading across platforms
8. ✅ Demonstrate visual evidence-based documentation approach

**Legend**: ✅ Complete | ⏳ In Progress | ❌ Blocked

---

## Quick Start (Zero-Setup Execution)

### Prerequisites
- Python 3.8+
- Windows enterprise environment (encoding-safe)

### Run the PoC
```batch
REM From any subdirectory within Project 10
run_mkdocs_poc.bat
```

The professional runner will:
1. Auto-detect project structure
2. Validate environment (pre-flight checks)
3. Generate MkDocs sample site
4. Build static HTML
5. Generate test validation checklist
6. Collect evidence artifacts

### Manual Execution (for development)
```powershell
cd docs\eva-foundation\projects\10-MkDocs-PoC
python scripts\build_mkdocs.py
```

---

## Project Structure

```
10-MkDocs-PoC/
├── README.md                          # This file
├── .github/
│   └── copilot-instructions.md        # Copilot configuration
├── scripts/
│   ├── build_mkdocs.py                # Main builder (professional runner)
│   ├── test_hosting.py                # Hosting validation tests
│   └── components/
│       ├── __init__.py
│       ├── mkdocs_generator.py        # MkDocs site generator
│       ├── evidence_collector.py      # Debug artifact collection
│       └── validation_reporter.py     # Test report generation
├── mkdocs-sample/                     # Generated MkDocs site
│   ├── mkdocs.yml                     # MkDocs configuration
│   ├── docs/                          # Source Markdown files
│   │   ├── index.md
│   │   ├── getting-started.md
│   │   ├── architecture/
│   │   │   ├── overview.md
│   │   │   └── data-flow.md
│   │   ├── governance/
│   │   │   ├── principles.md
│   │   │   └── audit-logging.md
│   │   ├── ops/
│   │   │   └── runbook.md
│   │   └── assets/                    # **98+ REAL EVA production assets**
│   │       ├── branding/              # SVG logos, favicon (4 files)
│   │       ├── docs-images/           # Screenshots, diagrams (80+ files)
│   │       ├── root-docs/             # Process flows, PDFs (10+ files)
│   │       └── diagrams/              # Diagram standards (SVG/PNG)
│   └── site/                          # Generated static HTML (after build)
├── debug/                             # Debug artifacts (MANDATORY)
│   ├── screenshots/                   # UI operation captures
│   ├── html/                          # Page state captures
│   └── traces/                        # Network/API traces
├── evidence/                          # Test evidence (MANDATORY)
│   └── test-results/
│       ├── spo-test-{timestamp}.json
│       └── azure-test-{timestamp}.json
├── logs/                              # Execution logs (MANDATORY)
├── sessions/                          # Session state persistence
├── output/                            # Generated reports
│   └── test-reports/
├── requirements-core.txt              # Core dependencies (MkDocs)
├── requirements-test.txt              # Testing dependencies
├── run_mkdocs_poc.bat                 # Windows-safe execution wrapper
└── VALIDATION-CHECKLIST.md            # Manual test validation guide
```

---

## MkDocs Sample Content

The generated sample site includes **real EVA production assets** demonstrating visual evidence-based documentation:

### Asset Integration (98+ Files from EVA-JP-reference-0113)
- ✅ **Architecture Diagrams**: Secure deployment, process flows, vector search (10+ diagrams)
- ✅ **UI Screenshots**: Chat interfaces, content management, upload workflows (17+ screenshots)
- ✅ **Feature Demos**: Work+Web, Math Assistant, Data Assist, governance panels (18+ demos)
- ✅ **Deployment Guides**: App registration, Cosmos DB, authentication configs (10+ guides)
- ✅ **Development**: Codespaces, VS Code, Python environment setup (15+ screenshots)
- ✅ **Debugging**: FastAPI logs, Functions, frontend watch, known issues (11+ captures)
- ✅ **Branding**: SVG logos (GitHub, OpenAI, Azure Search), favicon
- ✅ **Reference Docs**: Architecture PDFs, process flow diagrams

**Source Inventory**: [eva-da-ref-assets.md](../09-EVA-Repo-documentation/eva-da-ref-assets.md) (Project 09)

### Content Validation Points
- ✅ **Navigation**: Multi-level sidebar (Home, Getting Started, Architecture, Governance, Operations)
- ✅ **Internal Links**: Cross-references between pages
- ✅ **Deep Links**: Anchor links to specific sections
- ✅ **Tables**: Structured data presentation
- ✅ **Callouts**: Admonitions (note, warning, important, tip)
- ✅ **Code Blocks**: Syntax-highlighted examples
- ✅ **Images**: Asset path references
- ✅ **Headings**: Proper hierarchy (H1-H4)

### Example Pages
- **Home** (`index.md`) - Landing page with quick links
- **Getting Started** - Build/deploy instructions
- **Architecture Overview** - System components, constraints
- **Data Flow** - Request lifecycle with pseudocode
- **Governance Principles** - Non-negotiables, accountability
- **Audit Logging** - Event fields table with deep-link anchor
- **Operations Runbook** - Hosting test checklist

---

## Hosting Test Strategy

### Test 1: SharePoint Online Document Library

**Hypothesis**: SPO may download `.html` files instead of rendering them inline.

**Test Steps**:
1. Upload `mkdocs-sample/site/` contents to SPO document library
2. Click `index.html` and observe behavior
3. Validate:
   - ❓ Does HTML render in browser or force download?
   - ❓ Do CSS/JS assets load correctly?
   - ❓ Do relative links work?
   - ❓ Do deep links (anchors) work?

**Expected Issues**:
- SPO may serve `.html` with incorrect MIME types
- SPO may block JavaScript execution
- Relative paths may break in subfolder contexts

**Evidence Collection**:
- Screenshots of rendering behavior
- Network trace of asset loading
- Browser console errors
- Detailed test report in `evidence/test-results/spo-test-{timestamp}.json`

### Test 2: Azure Static Website (Baseline)

**Hypothesis**: Azure Static Website will reliably render MkDocs output.

**Test Steps**:
1. Create Azure Storage Account with Static Website enabled
2. Upload `mkdocs-sample/site/` contents to `$web` container
3. Access primary endpoint URL
4. Validate all content rendering correctly

**Expected Result**: ✅ All validation points pass (this is the reliable baseline)

**Evidence Collection**:
- Screenshots of rendered pages
- Network trace of asset loading
- Performance metrics
- Detailed test report in `evidence/test-results/azure-test-{timestamp}.json`

---

## Validation Checklist

See [VALIDATION-CHECKLIST.md](./VALIDATION-CHECKLIST.md) for detailed manual test steps.  
See [DEPLOYMENT-GUIDE.md](./DEPLOYMENT-GUIDE.md) for complete deployment procedures.

**Quick Validation**:
- [x] MkDocs site builds without errors (validated with `mkdocs build`)
- [x] Link validation script created (`mkdocs-sample/scripts/validate_links.py`)
- [ ] Navigation sidebar renders correctly (manual browser test required)
- [ ] Internal links navigate correctly (run link validator)
- [ ] Deep links scroll to anchors (manual test required)
- [ ] Tables render properly (manual test required)
- [ ] Callouts/admonitions display correctly (manual test required)
- [ ] Code blocks have syntax highlighting (manual test required)
- [ ] CSS/JS assets load without 404s (check browser DevTools)
- [ ] Mobile responsive design works (manual test required)

---

## Success Criteria

### Phase 1: Generation ✅ **COMPLETE**
- [x] MkDocs sample site generates successfully
- [x] All content validation points implemented (19 pages, 103 assets)
- [x] Professional runner with zero-setup execution
- [x] Evidence collection infrastructure operational
- [x] Link validation script created (Python stdlib + BeautifulSoup)
- [x] Deployment guide documented

### Phase 2: SharePoint Online Testing ⏳ **READY TO START**
- [ ] Upload site to SPO document library (see DEPLOYMENT-GUIDE.md)
- [ ] Document rendering behavior (render vs download)
- [ ] Validate asset loading (browser DevTools)
- [ ] Test deep links and navigation
- [ ] Generate detailed test report (evidence/test-results/)

### Phase 3: Azure Static Website Testing ⏳ **READY TO START**
- [ ] Deploy to Azure Storage Static Website (see DEPLOYMENT-GUIDE.md)
- [ ] Validate baseline functionality
- [ ] Performance baseline established (DevTools Performance tab)
- [ ] Generate detailed test report (evidence/test-results/)

### Phase 4: Analysis & Recommendation ⏳ **BLOCKED** (Requires Phase 2 & 3)
- [ ] Compare SPO vs Azure hosting results
- [ ] Document pros/cons of each approach
- [ ] Recommend hosting strategy for EVA docs
- [ ] Update README with final recommendation

**Known Limitations**:
- PNG diagram placeholders intentional (SVG-first strategy, PNG generated on-demand if needed)
- Selenium browser automation unavailable in enterprise Python repos (manual testing required)
- WCAG accessibility testing via browser extensions (axe DevTools, WAVE, Lighthouse)

---

## Technology Stack

- **MkDocs**: Static site generator (Python-based)
- **Python 3.8+**: Core runtime
- **Markdown**: Authoring format
- **SharePoint Online**: Test hosting platform (enterprise)
- **Azure Storage**: Baseline hosting platform (static website)

---

## Key Findings (To Be Updated Post-Testing)

### SharePoint Online
- **Rendering**: TBD after testing
- **Asset Loading**: TBD after testing
- **Navigation**: TBD after testing
- **Recommendation**: TBD

### Azure Static Website
- **Rendering**: TBD after testing
- **Asset Loading**: TBD after testing
- **Navigation**: TBD after testing
- **Recommendation**: TBD

---

## References

- [MkDocs Documentation](https://www.mkdocs.org/)
- [MkDocs Material Theme](https://squidfunk.github.io/mkdocs-material/)
- [Azure Static Web Apps](https://docs.microsoft.com/en-us/azure/static-web-apps/)
- [SharePoint Online Modern Experience](https://docs.microsoft.com/en-us/sharepoint/modern-experience)

---

## Maintainers

- **Marco Presta** - Project Owner
- **EVA Foundation Team** - Documentation Standards

---

## Change Log

| Date | Activity | Description | Author |
|------|----------|-------------|--------|
| 2026-01-24 | Initialization | Project scaffolding with EVA best practices applied | Marco Presta |
| 2026-01-24 | Implementation | MkDocs sample site generated, professional runner implemented | Marco Presta |
