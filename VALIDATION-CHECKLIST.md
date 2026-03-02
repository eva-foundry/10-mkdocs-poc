# MkDocs PoC - Validation Checklist

**Purpose**: Manual validation checklist for testing MkDocs hosting on SharePoint Online and Azure Static Website.  
**Date**: January 24, 2026  
**Project**: 10-MkDocs-PoC

---

## Prerequisites

### Required Access
- **Azure Subscription**: Active subscription with Contributor or Owner role for resource creation
- **SharePoint Online**: Access to SharePoint site with document library creation permissions (Site Member or higher)
- **Azure CLI**: Installed and authenticated (`az login` completed)

### Required Tools
- Python 3.8+ with MkDocs installed
- Web browser (Edge, Chrome, or Firefox recommended)
- Browser DevTools knowledge for evidence collection
- Screenshot tool (built-in Windows Snipping Tool or ShareX)

### Required Permissions
- **Azure**: Contributor or Owner role on subscription or resource group
- **SharePoint**: Site Member or Site Owner permissions for document library management

### Cost Considerations
- **Azure Storage Account**: ~$0.01-0.05/month for static website hosting
- **Test Duration**: Recommend completing tests within 1-2 hours to minimize costs
- **Cleanup**: Delete Azure resources immediately after testing (see Part 4 of DEPLOYMENT-GUIDE.md)

---

## Pre-Testing Setup

### Build MkDocs Site
- [ ] Run `run_mkdocs_poc.bat` to generate site
- [ ] Verify `mkdocs-sample/site/` directory exists
- [ ] Verify `mkdocs-sample/site/index.html` exists
- [ ] Check build logs in `logs/` directory

---

## Test 1: SharePoint Online Document Library Hosting

### Setup Steps
1. [ ] Navigate to SharePoint Online site
2. [ ] Create or select a document library
3. [ ] Upload contents of `mkdocs-sample/site/` folder:
   - [ ] Upload all `.html` files
   - [ ] Upload `css/` directory
   - [ ] Upload `js/` directory
   - [ ] Upload `search/` directory (if exists)
   - [ ] Upload `img/` directory (if exists)

### Validation Tests

#### Test 1.1: Homepage Rendering
- [ ] Click on `index.html` in SharePoint
- [ ] **Record behavior**:
  - [ ] ✅ HTML renders in browser
  - [ ] ❌ HTML file downloads instead of rendering
- [ ] Take screenshot and save to `evidence/test-results/spo-homepage-render.png`

#### Test 1.2: CSS Loading
- [ ] Open browser developer tools (F12)
- [ ] Navigate to Network tab
- [ ] Refresh page
- [ ] **Verify CSS files**:
  - [ ] ✅ CSS files load (200 status)
  - [ ] ❌ CSS files fail to load (404 or blocked)
- [ ] Take screenshot of Network tab and save to `evidence/test-results/spo-css-loading.png`

#### Test 1.3: JavaScript Loading
- [ ] Check Network tab for JavaScript files
- [ ] **Verify JS files**:
  - [ ] ✅ JS files load (200 status)
  - [ ] ❌ JS files fail to load (404 or blocked)
  - [ ] ❌ JS files blocked by SharePoint security
- [ ] Check Console tab for JavaScript errors
- [ ] Take screenshot and save to `evidence/test-results/spo-js-loading.png`

#### Test 1.4: Navigation Sidebar
- [ ] **Verify navigation menu**:
  - [ ] ✅ Sidebar displays correctly
  - [ ] ✅ Navigation items are clickable
  - [ ] ❌ Sidebar is missing or broken
- [ ] Click "Getting Started" link
- [ ] **Record navigation behavior**:
  - [ ] ✅ Navigation works within SharePoint
  - [ ] ❌ Navigation opens new browser tab
  - [ ] ❌ Navigation downloads file instead of navigating
- [ ] Take screenshot and save to `evidence/test-results/spo-navigation.png`

#### Test 1.5: Internal Links
- [ ] From Homepage, click "Architecture Overview" link
- [ ] **Verify link behavior**:
  - [ ] ✅ Link navigates correctly
  - [ ] ❌ Link is broken (404)
  - [ ] ❌ Link downloads file
- [ ] Take screenshot and save to `evidence/test-results/spo-internal-links.png`

#### Test 1.6: Deep Links (Anchors)
- [ ] Navigate to Governance section
- [ ] Click "Audit logging fields" deep link
- [ ] **Verify anchor behavior**:
  - [ ] ✅ Page scrolls to correct section
  - [ ] ❌ Anchor link doesn't work
- [ ] Take screenshot and save to `evidence/test-results/spo-deep-links.png`

#### Test 1.7: Tables
- [ ] Navigate to "Audit Logging" page
- [ ] **Verify table rendering**:
  - [ ] ✅ Table displays correctly
  - [ ] ✅ Table formatting preserved
  - [ ] ❌ Table is broken or unstyled
- [ ] Take screenshot and save to `evidence/test-results/spo-tables.png`

#### Test 1.8: Callouts/Admonitions
- [ ] Navigate to "Getting Started" page
- [ ] **Verify callout boxes**:
  - [ ] ✅ Note/Warning/Tip boxes display correctly
  - [ ] ✅ Callout styling preserved
  - [ ] ❌ Callouts display as plain text
- [ ] Take screenshot and save to `evidence/test-results/spo-callouts.png`

#### Test 1.9: Code Blocks
- [ ] Navigate to "Data Flow" page
- [ ] **Verify code block rendering**:
  - [ ] ✅ Code blocks display correctly
  - [ ] ✅ Syntax highlighting works
  - [ ] ❌ Code blocks display as plain text
- [ ] Take screenshot and save to `evidence/test-results/spo-code-blocks.png`

#### Test 1.10: Mobile Responsiveness
- [ ] Resize browser window to mobile width (375px)
- [ ] **Verify responsive design**:
  - [ ] ✅ Layout adapts to mobile view
  - [ ] ✅ Navigation collapses to hamburger menu
  - [ ] ❌ Layout breaks on mobile
- [ ] Take screenshot and save to `evidence/test-results/spo-mobile-responsive.png`

### SharePoint Online Test Summary
- [ ] Document overall findings in `evidence/test-results/spo-test-summary.md`
- [ ] Rate overall experience (1-5 stars)
- [ ] Note critical blockers (if any)
- [ ] Provide recommendation (✅ Use SPO / ❌ Do NOT use SPO)

---

## Test 2: Azure Static Website Hosting (Baseline)

### Setup Steps
1. [ ] Create Azure Storage Account (or use existing)
2. [ ] Enable Static Website hosting on Storage Account
3. [ ] Note primary endpoint URL
4. [ ] Upload contents of `mkdocs-sample/site/` to `$web` container:
   - [ ] Use Azure Portal Storage Browser
   - [ ] Or use Azure CLI: `az storage blob upload-batch`
   - [ ] Or use Azure Storage Explorer

### Validation Tests

#### Test 2.1: Homepage Rendering
- [ ] Navigate to primary endpoint URL
- [ ] **Verify homepage**:
  - [ ] ✅ Homepage loads successfully
  - [ ] ✅ Page title displays correctly
  - [ ] ❌ Homepage fails to load
- [ ] Take screenshot and save to `evidence/test-results/azure-homepage-render.png`

#### Test 2.2: Asset Loading
- [ ] Open browser developer tools (F12)
- [ ] Navigate to Network tab
- [ ] Refresh page
- [ ] **Verify all assets**:
  - [ ] ✅ All CSS files load (200 status)
  - [ ] ✅ All JS files load (200 status)
  - [ ] ✅ All images load (200 status)
  - [ ] ❌ Any assets fail to load (note which ones)
- [ ] Take screenshot of Network tab and save to `evidence/test-results/azure-asset-loading.png`

#### Test 2.3: Navigation
- [ ] Click through all navigation items
- [ ] **Verify navigation**:
  - [ ] ✅ All pages accessible
  - [ ] ✅ Navigation preserves context
  - [ ] ❌ Any navigation issues (note which)
- [ ] Take screenshot and save to `evidence/test-results/azure-navigation.png`

#### Test 2.4: Internal Links
- [ ] Test all internal links
- [ ] **Verify links**:
  - [ ] ✅ All internal links work
  - [ ] ❌ Any broken links (note which)
- [ ] Take screenshot and save to `evidence/test-results/azure-internal-links.png`

#### Test 2.5: Deep Links (Anchors)
- [ ] Test deep link to "Audit event fields" section
- [ ] **Verify anchor behavior**:
  - [ ] ✅ Page scrolls to correct section
  - [ ] ❌ Anchor link doesn't work
- [ ] Take screenshot and save to `evidence/test-results/azure-deep-links.png`

#### Test 2.6: Content Rendering
- [ ] Verify tables render correctly
- [ ] Verify callouts/admonitions display correctly
- [ ] Verify code blocks display with syntax highlighting
- [ ] **Overall content rendering**:
  - [ ] ✅ All content renders perfectly
  - [ ] ❌ Any content rendering issues (note which)
- [ ] Take screenshot and save to `evidence/test-results/azure-content-rendering.png`

#### Test 2.7: Performance
- [ ] Check Network tab for page load time
- [ ] **Record performance metrics**:
  - Homepage load time: _____ ms
  - Largest Contentful Paint (LCP): _____ ms
  - First Input Delay (FID): _____ ms
  - Cumulative Layout Shift (CLS): _____
- [ ] Take screenshot and save to `evidence/test-results/azure-performance.png`

#### Test 2.8: Mobile Responsiveness
- [ ] Test on mobile device or responsive mode
- [ ] **Verify responsive design**:
  - [ ] ✅ Layout adapts correctly
  - [ ] ✅ Navigation works on mobile
  - [ ] ❌ Any mobile issues (note which)
- [ ] Take screenshot and save to `evidence/test-results/azure-mobile-responsive.png`

### Azure Static Website Test Summary
- [ ] Document overall findings in `evidence/test-results/azure-test-summary.md`
- [ ] Rate overall experience (1-5 stars)
- [ ] Note any issues (should be minimal for Azure)
- [ ] Confirm baseline functionality

---

## Comparison Analysis

### Feature Comparison

| Feature | SharePoint Online | Azure Static Website |
|---------|-------------------|----------------------|
| HTML Rendering | [ ] Pass / [ ] Fail | [ ] Pass / [ ] Fail |
| CSS Loading | [ ] Pass / [ ] Fail | [ ] Pass / [ ] Fail |
| JS Loading | [ ] Pass / [ ] Fail | [ ] Pass / [ ] Fail |
| Navigation | [ ] Pass / [ ] Fail | [ ] Pass / [ ] Fail |
| Internal Links | [ ] Pass / [ ] Fail | [ ] Pass / [ ] Fail |
| Deep Links | [ ] Pass / [ ] Fail | [ ] Pass / [ ] Fail |
| Tables | [ ] Pass / [ ] Fail | [ ] Pass / [ ] Fail |
| Callouts | [ ] Pass / [ ] Fail | [ ] Pass / [ ] Fail |
| Code Blocks | [ ] Pass / [ ] Fail | [ ] Pass / [ ] Fail |
| Mobile Responsive | [ ] Pass / [ ] Fail | [ ] Pass / [ ] Fail |
| Performance | _____ rating | _____ rating |
| Ease of Setup | _____ rating | _____ rating |

### Overall Recommendation

Based on testing results:

**SharePoint Online**:
- [ ] ✅ Recommended for EVA documentation
- [ ] ❌ NOT recommended for EVA documentation

**Reasoning**: _________________________________

**Azure Static Website**:
- [ ] ✅ Recommended for EVA documentation
- [ ] ❌ NOT recommended for EVA documentation

**Reasoning**: _________________________________

**Final Recommendation**: _________________________________

---

## Post-Testing Activities

- [ ] Generate consolidated test report in `output/test-reports/`
- [ ] Update Project 10 README.md with findings
- [ ] Document recommended hosting strategy
- [ ] Create deployment guide for chosen platform
- [ ] Archive all evidence artifacts
- [ ] Present findings to EVA Foundation team

---

## Notes

Use this section for additional observations:

```
[Add notes here]
```
