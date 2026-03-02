# MkDocs PoC - Deployment Guide

**Purpose**: Step-by-step deployment procedures for SharePoint Online and Azure Static Website hosting tests  
**Date**: January 24, 2026  
**Project**: 10-MkDocs-PoC

---

## Prerequisites

### Required Access
- **Azure Subscription**: Active subscription with Contributor or Owner role
- **SharePoint Online**: Access to SharePoint site with document library creation permissions
- **Azure CLI**: Installed and authenticated (`az login`)

### Required Tools
- Python 3.8+ with MkDocs installed
- Azure CLI version 2.30.0 or higher
- Web browser (Edge, Chrome, Firefox)
- Browser DevTools knowledge for evidence collection

### Cost Considerations
- **Azure Storage Account**: ~$0.01-0.05/month for static website hosting
- **SharePoint Online**: Included in Microsoft 365 subscription (no additional cost)

---

## Part 1: Build MkDocs Site

### Step 1: Generate and Build Site

```powershell
# Navigate to mkdocs-sample directory
cd docs\eva-foundation\projects\10-MkDocs-PoC\mkdocs-sample

# Build static HTML (generates site/ directory)
python -m mkdocs build

# Verify build succeeded
if (Test-Path "site\index.html") {
    Write-Host "[SUCCESS] Site built successfully" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Build failed - site\index.html not found" -ForegroundColor Red
    exit 1
}
```

### Step 2: Validate Links

```powershell
# Run link validation script
python scripts\validate_links.py

# Check evidence report
Get-Content "..\evidence\test-results\link_validation_*.json" | ConvertFrom-Json | Select-Object -ExpandProperty summary
```

**Expected Result**: Status = "PASS", broken_links = 0, broken_images = 0

---

## Part 2: SharePoint Online Deployment

### Prerequisites
- SharePoint site URL (e.g., `https://yourorg.sharepoint.com/sites/your-site`)
- Document library creation permissions
- Browser access to SharePoint

### Step 1: Create Document Library

1. Navigate to your SharePoint site
2. Click **New** → **Document library**
3. Name: `EVA-MkDocs-Test`
4. Description: "MkDocs PoC hosting test - Static HTML validation"
5. Click **Create**

### Step 2: Upload Site Files

**Option A: Via SharePoint Web Interface**

1. Open the `EVA-MkDocs-Test` library
2. Click **Upload** → **Files**
3. Navigate to `mkdocs-sample\site\` directory
4. Select ALL files and folders (Ctrl+A)
5. Click **Open** to start upload
6. Wait for upload completion (may take 5-10 minutes for 100+ files)

**Important**: SharePoint maintains folder structure automatically.

**Option B: Via OneDrive Sync (Faster for Large Uploads)**

1. Click **Sync** button in SharePoint library toolbar
2. Wait for OneDrive to sync the library to local folder
3. Copy contents of `mkdocs-sample\site\` to synced folder
4. OneDrive will upload automatically
5. Wait for green checkmarks (sync complete)

### Step 3: Test Rendering

1. Navigate to `EVA-MkDocs-Test` library in browser
2. Click on `index.html` file

**Critical Test**: Does the HTML file:
- ✅ Render in browser with proper formatting?
- ❌ Download as a file instead of rendering?

### Step 4: Collect Evidence

Open browser DevTools (F12) and collect:

1. **Screenshot of rendered page**: `evidence/test-results/spo-homepage-render.png`
2. **Network tab**: Check CSS/JS file loading status codes
3. **Console tab**: Check for JavaScript errors
4. **Test navigation**: Click internal links, verify they work

**Evidence Checklist**:
- [ ] Homepage screenshot (rendered or download dialog)
- [ ] Network tab screenshot (asset loading status)
- [ ] Console tab screenshot (JavaScript errors if any)
- [ ] Navigation test screenshot (clicking Getting Started link)

### Step 5: Document Findings

Create `evidence/test-results/spo-test-summary.md`:

```markdown
# SharePoint Online Test Results

**Date**: [YYYY-MM-DD]  
**Tester**: [Your Name]  
**SharePoint Site**: [URL]

## Test Results

### Test 1.1: Homepage Rendering
- Result: [PASS/FAIL]
- Behavior: [Rendered in browser / Downloaded as file]
- Screenshot: spo-homepage-render.png

### Test 1.2: CSS Loading
- Result: [PASS/FAIL]
- Status codes: [200 OK / 404 Not Found / Blocked]
- Screenshot: spo-css-loading.png

### Test 1.3: JavaScript Loading
- Result: [PASS/FAIL]
- Status codes: [200 OK / 404 Not Found / Blocked]
- Console errors: [List any errors]
- Screenshot: spo-js-loading.png

### Test 1.4: Navigation
- Result: [PASS/FAIL]
- Behavior: [Navigated in same window / Opened new tab / Downloaded]
- Screenshot: spo-navigation.png

## Overall Assessment

**Recommendation**: [✅ Use SPO / ❌ Do NOT use SPO]

**Reasoning**: [Explain findings]
```

---

## Part 3: Azure Static Website Deployment

### Step 1: Create Storage Account

```powershell
# Set variables
$resourceGroup = "rg-eva-mkdocs-test"
$location = "canadacentral"
$storageAccount = "stgevamkdocstest"  # Must be globally unique, lowercase, no hyphens

# Create resource group
az group create --name $resourceGroup --location $location

# Create storage account
az storage account create `
    --name $storageAccount `
    --resource-group $resourceGroup `
    --location $location `
    --sku Standard_LRS `
    --kind StorageV2 `
    --allow-blob-public-access true

Write-Host "[SUCCESS] Storage account created" -ForegroundColor Green
```

### Step 2: Enable Static Website Hosting

```powershell
# Enable static website
az storage blob service-properties update `
    --account-name $storageAccount `
    --static-website `
    --404-document 404.html `
    --index-document index.html

# Get primary endpoint URL
$endpoint = az storage account show `
    --name $storageAccount `
    --resource-group $resourceGroup `
    --query "primaryEndpoints.web" `
    --output tsv

Write-Host "[INFO] Static website endpoint: $endpoint" -ForegroundColor Cyan
```

### Step 3: Upload Site Files

```powershell
# Upload all files to $web container
az storage blob upload-batch `
    --account-name $storageAccount `
    --source "mkdocs-sample\site" `
    --destination '$web' `
    --overwrite

Write-Host "[SUCCESS] Files uploaded to $web container" -ForegroundColor Green
```

### Step 4: Test Access

```powershell
# Open in default browser
Start-Process $endpoint
```

**Verification**:
1. Homepage loads with proper styling
2. Navigation sidebar displays correctly
3. Internal links work
4. Images load without 404 errors
5. Search functionality works (if enabled)

### Step 5: Collect Evidence

Open browser DevTools (F12) and collect:

1. **Screenshot of homepage**: `evidence/test-results/azure-homepage-render.png`
2. **Network tab**: Verify all assets load (200 status)
3. **Performance tab**: Record page load metrics
4. **Lighthouse audit**: Run accessibility/performance scan

**Evidence Checklist**:
- [ ] Homepage screenshot
- [ ] Network tab screenshot (all assets 200 OK)
- [ ] Performance metrics screenshot
- [ ] Navigation test screenshot
- [ ] Mobile responsiveness screenshot

### Step 6: Collect Performance Metrics

In browser DevTools:

1. Open **Performance** tab
2. Click **Reload** to record page load
3. Note metrics:
   - **Load time**: _____ ms
   - **DOMContentLoaded**: _____ ms
   - **First Contentful Paint (FCP)**: _____ ms
   - **Largest Contentful Paint (LCP)**: _____ ms

### Step 7: Document Findings

Create `evidence/test-results/azure-test-summary.md`:

```markdown
# Azure Static Website Test Results

**Date**: [YYYY-MM-DD]  
**Tester**: [Your Name]  
**Endpoint**: [Static website URL]

## Test Results

### Test 2.1: Homepage Rendering
- Result: PASS
- Load time: _____ ms
- Screenshot: azure-homepage-render.png

### Test 2.2: Asset Loading
- Result: PASS
- CSS files: All 200 OK
- JS files: All 200 OK
- Images: All 200 OK
- Screenshot: azure-asset-loading.png

### Test 2.3: Navigation
- Result: PASS
- All internal links functional
- Screenshot: azure-navigation.png

### Test 2.4: Performance
- Load time: _____ ms
- FCP: _____ ms
- LCP: _____ ms
- Screenshot: azure-performance.png

## Overall Assessment

**Recommendation**: ✅ Use Azure Static Website

**Reasoning**: Reliable static hosting, fast performance, proper MIME types, full functionality.
```

---

## Part 4: Cleanup (Cost Management)

### Delete Azure Resources

```powershell
# Delete entire resource group (removes all resources)
az group delete --name $resourceGroup --yes --no-wait

Write-Host "[INFO] Resource group deletion initiated" -ForegroundColor Yellow
Write-Host "[INFO] Resources will be deleted in background" -ForegroundColor Yellow
```

### Delete SharePoint Test Library

1. Navigate to SharePoint site
2. Go to **Site contents**
3. Find `EVA-MkDocs-Test` library
4. Click **...** (More options) → **Settings**
5. Scroll to bottom → **Delete this document library**
6. Confirm deletion

---

## Part 5: Evidence Collection Best Practices

### Screenshot Standards

**Format**: PNG (lossless compression)  
**Naming**: `{platform}-{test-id}-{description}.png`  
**Examples**:
- `spo-test1.1-homepage-render.png`
- `azure-test2.2-asset-loading.png`

### Browser DevTools Usage

**Network Tab Evidence**:
1. Open DevTools (F12)
2. Go to **Network** tab
3. Check **Preserve log**
4. Reload page (Ctrl+R)
5. Screenshot showing:
   - File names
   - Status codes (200, 404, etc.)
   - Load times

**Console Tab Evidence**:
1. Go to **Console** tab
2. Screenshot showing:
   - Any error messages (red)
   - Any warning messages (yellow)
   - Clean console (if no errors)

**Performance Tab Evidence**:
1. Go to **Performance** tab
2. Click **Reload** icon (record during page load)
3. Wait for recording to complete
4. Screenshot showing:
   - Load timeline
   - FCP/LCP markers
   - Total load time

### JSON Evidence Format

All automated tests should generate JSON with this structure:

```json
{
  "timestamp": "2026-01-24T15:30:00.000Z",
  "platform": "spo|azure",
  "test_id": "1.1|2.1|etc",
  "test_name": "Homepage Rendering",
  "result": "PASS|FAIL",
  "details": {
    "behavior": "Rendered in browser",
    "load_time_ms": 1234,
    "status_code": 200,
    "errors": []
  },
  "evidence_files": [
    "spo-homepage-render.png",
    "spo-css-loading.png"
  ]
}
```

---

## Troubleshooting

### SharePoint Issues

**Problem**: HTML downloads instead of rendering  
**Solution**: This is expected behavior. SharePoint document libraries serve files for download, not as web pages. Document this as a finding.

**Problem**: CSS/JS blocked by SharePoint  
**Solution**: SharePoint may block external scripts. Document this limitation. This is why Azure Static Website is the baseline comparison.

### Azure Issues

**Problem**: 404 on static website endpoint  
**Solution**: 
```powershell
# Verify static website is enabled
az storage blob service-properties show --account-name $storageAccount --query "staticWebsite.enabled"

# Should return "true"
```

**Problem**: Assets return 404  
**Solution**: Verify files uploaded to `$web` container:
```powershell
az storage blob list --account-name $storageAccount --container-name '$web' --output table
```

**Problem**: Endpoint URL not accessible  
**Solution**: Check blob public access is enabled:
```powershell
az storage account show --name $storageAccount --query "allowBlobPublicAccess"
```

---

## Next Steps

After completing both deployments:

1. **Compare Results**: Use comparison table in VALIDATION-CHECKLIST.md
2. **Generate Report**: Consolidate findings in `output/test-reports/`
3. **Make Recommendation**: Document which platform to use for EVA documentation
4. **Update Project Status**: Mark Phase 2 & 3 complete in README.md

---

## Security Notes

- **Azure Storage**: Blob public access enabled for static website hosting (required)
- **SharePoint**: Uses existing organizational security (Entra ID authentication)
- **Test Data**: No sensitive information in test documentation
- **Cleanup**: Delete resources after testing to avoid ongoing costs

---

## Questions?

Refer to:
- [VALIDATION-CHECKLIST.md](./VALIDATION-CHECKLIST.md) - Detailed test procedures
- [README.md](./README.md) - Project overview
- Azure Static Website Docs: https://learn.microsoft.com/azure/storage/blobs/storage-blob-static-website
