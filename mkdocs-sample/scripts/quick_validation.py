#!/usr/bin/env python3
"""Quick GCDS Theme Validation - No external dependencies"""

import os
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent

# Files to check
REQUIRED_FILES = [
    "gcds-theme/base.html",
    "gcds-theme/main.html",
    "gcds-theme/partials/nav.html",
    "gcds-theme/partials/toc.html",
    "docs/stylesheets/gcds-alerts.css",
    "docs/javascripts/gcds-collapsible.js",
    "docs/fr/under-construction.md",
    "site/index.html",
    "site/assets/gcds/gcds.css",
    "site/assets/gcds/gcds.esm.js"
]

GCDS_COMPONENTS = [
    "<gcds-header",
    "<gcds-container", 
    "<gcds-footer"
]

CSS_ALERT_CLASSES = [
    ".alert-info",
    ".alert-warning", 
    ".alert-danger",
    ".alert-success"
]

def check_files():
    """Check if all required files exist"""
    print("\n[1/4] Checking required files...")
    results = []
    for file_path in REQUIRED_FILES:
        full_path = PROJECT_ROOT / file_path
        exists = full_path.exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {file_path}")
        results.append({"file": file_path, "exists": exists})
    return results

def check_html_components():
    """Check if built HTML contains GCDS components"""
    print("\n[2/4] Checking GCDS components in built HTML...")
    index_path = PROJECT_ROOT / "site" / "index.html"
    
    if not index_path.exists():
        print("  ✗ site/index.html not found - build failed?")
        return {"error": "index.html not found"}
    
    with open(index_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    results = []
    for component in GCDS_COMPONENTS:
        found = component in html_content
        status = "✓" if found else "✗"
        print(f"  {status} {component}")
        results.append({"component": component, "found": found})
    
    return results

def check_css_alerts():
    """Check if CSS alert classes exist"""
    print("\n[3/4] Checking CSS alert classes...")
    css_path = PROJECT_ROOT / "docs" / "stylesheets" / "gcds-alerts.css"
    
    if not css_path.exists():
        print("  ✗ gcds-alerts.css not found")
        return {"error": "CSS file not found"}
    
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    results = []
    for css_class in CSS_ALERT_CLASSES:
        found = css_class in css_content
        status = "✓" if found else "✗"
        print(f"  {status} {css_class}")
        results.append({"class": css_class, "found": found})
    
    return results

def check_bilingual():
    """Check bilingual FR page"""
    print("\n[4/4] Checking bilingual support...")
    fr_page = PROJECT_ROOT / "docs" / "fr" / "under-construction.md"
    fr_built = PROJECT_ROOT / "site" / "fr" / "under-construction" / "index.html"
    
    results = []
    
    # Check source exists
    if fr_page.exists():
        print("  ✓ FR source page exists")
        results.append({"check": "FR source", "passed": True})
    else:
        print("  ✗ FR source page missing")
        results.append({"check": "FR source", "passed": False})
    
    # Check built page exists
    if fr_built.exists():
        print("  ✓ FR built page exists")
        results.append({"check": "FR built", "passed": True})
        
        # Check for lang-href in index.html
        index_path = PROJECT_ROOT / "site" / "index.html"
        with open(index_path, 'r', encoding='utf-8') as f:
            index_content = f.read()
        
        if 'lang-href="/fr/under-construction.html"' in index_content:
            print("  ✓ Language toggle configured")
            results.append({"check": "lang-href", "passed": True})
        else:
            print("  ✗ Language toggle not found")
            results.append({"check": "lang-href", "passed": False})
    else:
        print("  ✗ FR built page missing")
        results.append({"check": "FR built", "passed": False})
    
    return results

def main():
    print("=" * 60)
    print("  GCDS THEME QUICK VALIDATION")
    print("=" * 60)
    
    # Run all checks
    file_results = check_files()
    html_results = check_html_components()
    css_results = check_css_alerts()
    bilingual_results = check_bilingual()
    
    # Compile results
    validation_report = {
        "timestamp": datetime.now().isoformat(),
        "project_root": str(PROJECT_ROOT),
        "checks": {
            "file_checks": file_results,
            "html_components": html_results,
            "css_alerts": css_results,
            "bilingual": bilingual_results
        }
    }
    
    # Calculate overall status
    file_passed = all(r["exists"] for r in file_results)
    html_passed = isinstance(html_results, list) and all(r["found"] for r in html_results)
    css_passed = isinstance(css_results, list) and all(r["found"] for r in css_results)
    bilingual_passed = all(r["passed"] for r in bilingual_results)
    
    overall_passed = file_passed and html_passed and css_passed and bilingual_passed
    
    validation_report["overall_status"] = "PASS" if overall_passed else "PARTIAL"
    validation_report["summary"] = {
        "files": "PASS" if file_passed else "FAIL",
        "html": "PASS" if html_passed else "FAIL",
        "css": "PASS" if css_passed else "FAIL",
        "bilingual": "PASS" if bilingual_passed else "FAIL"
    }
    
    # Save results
    evidence_dir = PROJECT_ROOT / "evidence" / "test-results"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = evidence_dir / "gcds-quick-validation.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(validation_report, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 60)
    print("  VALIDATION SUMMARY")
    print("=" * 60)
    print(f"  Files:     {validation_report['summary']['files']}")
    print(f"  HTML:      {validation_report['summary']['html']}")
    print(f"  CSS:       {validation_report['summary']['css']}")
    print(f"  Bilingual: {validation_report['summary']['bilingual']}")
    print(f"\n  OVERALL:   {validation_report['overall_status']}")
    print(f"\n  Report saved: {output_path}")
    print("=" * 60)
    
    # Return exit code
    return 0 if overall_passed else 1

if __name__ == "__main__":
    exit(main())
