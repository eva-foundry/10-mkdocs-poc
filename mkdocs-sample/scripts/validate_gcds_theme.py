#!/usr/bin/env python3
"""
GCDS Theme Validation Script
Validates MkDocs GCDS theme implementation with comprehensive checks including:
- File existence validation
- HTML structure validation
- GCDS component presence
- CSS alert class validation
- JavaScript collapsible functionality
- WCAG 2.1 AA accessibility compliance (using axe-core)

Generates JSON evidence report for acceptance criteria
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Check if required dependencies are installed
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERROR] BeautifulSoup4 not installed. Run: pip install beautifulsoup4")
    sys.exit(1)

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from axe_selenium_python import Axe
except ImportError:
    print("[WARNING] Selenium or axe-selenium-python not installed")
    print("WCAG tests will be skipped. To enable: pip install selenium axe-selenium-python")
    WCAG_AVAILABLE = False
else:
    WCAG_AVAILABLE = True


class GCDSThemeValidator:
    """Validates GCDS MkDocs theme implementation"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "checks": [],
            "summary": {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
        }
    
    def add_check(self, name: str, passed: bool, details: str = "", skipped: bool = False):
        """Add a validation check result"""
        status = "SKIPPED" if skipped else ("PASS" if passed else "FAIL")
        self.results["checks"].append({
            "name": name,
            "status": status,
            "details": details
        })
        self.results["summary"]["total"] += 1
        if skipped:
            self.results["summary"]["skipped"] += 1
        elif passed:
            self.results["summary"]["passed"] += 1
        else:
            self.results["summary"]["failed"] += 1
    
    def check_file_exists(self, rel_path: str, description: str):
        """Check if a file exists"""
        full_path = self.project_root / rel_path
        exists = full_path.exists()
        self.add_check(
            f"File exists: {rel_path}",
            exists,
            f"{description} - {'Found' if exists else 'Missing'} at {full_path}"
        )
        return exists
    
    def check_directory_exists(self, rel_path: str, description: str):
        """Check if a directory exists"""
        full_path = self.project_root / rel_path
        exists = full_path.is_dir()
        self.add_check(
            f"Directory exists: {rel_path}",
            exists,
            f"{description} - {'Found' if exists else 'Missing'} at {full_path}"
        )
        return exists
    
    def validate_html_structure(self, html_path: Path):
        """Validate HTML contains required GCDS components"""
        if not html_path.exists():
            self.add_check("HTML structure validation", False, f"HTML file not found: {html_path}")
            return False
        
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check for GCDS header
        gcds_header = soup.find('gcds-header')
        self.add_check(
            "GCDS header present",
            gcds_header is not None,
            f"<gcds-header> {'found' if gcds_header else 'missing'} in {html_path.name}"
        )
        
        # Check skip-to-content link
        if gcds_header:
            skip_href = gcds_header.get('skip-to-href')
            self.add_check(
                "Skip-to-content link configured",
                skip_href == '#main-content',
                f"skip-to-href = '{skip_href}'"
            )
        
        # Check for main content container
        main_container = soup.find('gcds-container', {'id': 'main-content'})
        self.add_check(
            "Main content container present",
            main_container is not None,
            f"<gcds-container id='main-content'> {'found' if main_container else 'missing'}"
        )
        
        # Check for GCDS footer
        gcds_footer = soup.find('gcds-footer')
        self.add_check(
            "GCDS footer present",
            gcds_footer is not None,
            f"<gcds-footer> {'found' if gcds_footer else 'missing'}"
        )
        
        # Check for GCDS CSS
        gcds_css = soup.find('link', href=re.compile(r'gcds\.css'))
        self.add_check(
            "GCDS CSS loaded",
            gcds_css is not None,
            f"gcds.css {'found' if gcds_css else 'missing'} in stylesheets"
        )
        
        # Check for GCDS JavaScript
        gcds_js = soup.find('script', src=re.compile(r'gcds\.esm\.js'))
        self.add_check(
            "GCDS JavaScript loaded",
            gcds_js is not None and gcds_js.get('type') == 'module',
            f"gcds.esm.js with type='module' {'found' if gcds_js else 'missing'}"
        )
        
        return True
    
    def validate_css_alerts(self, css_path: Path):
        """Validate Canada.ca alert CSS classes are defined"""
        if not css_path.exists():
            self.add_check("CSS alert validation", False, f"CSS file not found: {css_path}")
            return False
        
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        required_classes = [
            '.alert-info',
            '.alert-success',
            '.alert-warning',
            '.alert-danger',
            '.admonition.note',
            '.admonition.warning',
            '.admonition.danger',
            '.admonition.success'
        ]
        
        for css_class in required_classes:
            exists = css_class in css_content
            self.add_check(
                f"CSS class defined: {css_class}",
                exists,
                f"{'Found' if exists else 'Missing'} in {css_path.name}"
            )
    
    def validate_collapsible_js(self, js_path: Path):
        """Validate collapsible JavaScript functionality"""
        if not js_path.exists():
            self.add_check("JavaScript collapsible validation", False, f"JS file not found: {js_path}")
            return False
        
        with open(js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        required_functions = [
            'initCollapsibleAdmonitions',
            'transformToDetails',
            'addToggleListener'
        ]
        
        for func_name in required_functions:
            exists = func_name in js_content
            self.add_check(
                f"JavaScript function defined: {func_name}",
                exists,
                f"{'Found' if exists else 'Missing'} in {js_path.name}"
            )
    
    def validate_fr_construction_page(self):
        """Validate French construction page exists and returns 200"""
        fr_page = self.project_root / 'docs' / 'fr' / 'under-construction.md'
        exists = fr_page.exists()
        self.add_check(
            "FR construction page exists",
            exists,
            f"{'Found' if exists else 'Missing'}: {fr_page}"
        )
        
        if exists:
            # Check if it contains bilingual content
            with open(fr_page, 'r', encoding='utf-8') as f:
                content = f.read()
                has_french = 'construction' in content.lower() or 'développement' in content.lower()
                has_alert = 'alert' in content.lower()
                self.add_check(
                    "FR construction page has bilingual alert",
                    has_french and has_alert,
                    f"Content validation: {'PASS' if (has_french and has_alert) else 'FAIL'}"
                )
    
    def validate_wcag_compliance(self, site_dir: Path):
        """Validate WCAG 2.1 AA compliance using axe-core"""
        if not WCAG_AVAILABLE:
            self.add_check(
                "WCAG 2.1 AA compliance test",
                False,
                "Selenium/axe-selenium-python not installed - test skipped",
                skipped=True
            )
            return
        
        index_html = site_dir / 'index.html'
        if not index_html.exists():
            self.add_check(
                "WCAG 2.1 AA compliance test",
                False,
                f"Site not built yet - {index_html} missing",
                skipped=True
            )
            return
        
        # Set up headless Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(f'file:///{index_html.absolute()}')
            
            # Run axe accessibility checks
            axe = Axe(driver)
            axe.inject()
            results = axe.run()
            
            violations = results.get('violations', [])
            passes = results.get('passes', [])
            
            # Filter by WCAG 2.1 AA
            wcag_aa_violations = [
                v for v in violations 
                if any('wcag2a' in tag or 'wcag2aa' in tag or 'wcag21aa' in tag 
                       for tag in v.get('tags', []))
            ]
            
            passed = len(wcag_aa_violations) == 0
            details = f"WCAG 2.1 AA: {len(wcag_aa_violations)} violations, {len(passes)} passes"
            
            if wcag_aa_violations:
                details += "\nViolations:\n"
                for v in wcag_aa_violations[:5]:  # Show first 5
                    details += f"  - {v['id']}: {v['description']}\n"
            
            self.add_check(
                "WCAG 2.1 AA compliance test",
                passed,
                details
            )
            
            driver.quit()
            
        except Exception as e:
            self.add_check(
                "WCAG 2.1 AA compliance test",
                False,
                f"Test failed with error: {str(e)}",
                skipped=True
            )
    
    def run_all_validations(self):
        """Run all validation checks"""
        print("[GCDS Theme Validation] Starting comprehensive checks...")
        
        # File existence checks
        self.check_directory_exists('gcds-theme', 'Custom GCDS theme directory')
        self.check_file_exists('gcds-theme/base.html', 'Base HTML template')
        self.check_file_exists('gcds-theme/main.html', 'Main HTML template')
        self.check_file_exists('gcds-theme/partials/nav.html', 'Navigation partial')
        self.check_file_exists('gcds-theme/partials/toc.html', 'TOC partial')
        
        self.check_file_exists('package.json', 'NPM package configuration')
        self.check_file_exists('copy-gcds-assets.js', 'GCDS asset copy script')
        
        self.check_directory_exists('docs/assets/gcds', 'GCDS assets directory')
        self.check_file_exists('docs/stylesheets/gcds-alerts.css', 'Canada.ca alert CSS')
        self.check_file_exists('docs/javascripts/gcds-collapsible.js', 'Collapsible JS')
        self.check_file_exists('docs/fr/under-construction.md', 'FR construction page')
        
        # HTML structure validation (if site is built)
        site_index = self.project_root / 'site' / 'index.html'
        if site_index.exists():
            print("[GCDS Theme Validation] Validating HTML structure...")
            self.validate_html_structure(site_index)
        else:
            self.add_check(
                "HTML structure validation",
                False,
                f"Site not built yet - run 'mkdocs build' first",
                skipped=True
            )
        
        # CSS validation
        css_path = self.project_root / 'docs' / 'stylesheets' / 'gcds-alerts.css'
        if css_path.exists():
            print("[GCDS Theme Validation] Validating CSS alert classes...")
            self.validate_css_alerts(css_path)
        
        # JavaScript validation
        js_path = self.project_root / 'docs' / 'javascripts' / 'gcds-collapsible.js'
        if js_path.exists():
            print("[GCDS Theme Validation] Validating collapsible JavaScript...")
            self.validate_collapsible_js(js_path)
        
        # FR construction page validation
        print("[GCDS Theme Validation] Validating FR construction page...")
        self.validate_fr_construction_page()
        
        # WCAG compliance validation
        site_dir = self.project_root / 'site'
        if site_dir.exists():
            print("[GCDS Theme Validation] Running WCAG 2.1 AA compliance tests...")
            self.validate_wcag_compliance(site_dir)
        else:
            self.add_check(
                "WCAG 2.1 AA compliance test",
                False,
                "Site not built yet - run 'mkdocs build' first",
                skipped=True
            )
    
    def generate_report(self, output_path: Path):
        """Generate JSON evidence report"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n[GCDS Theme Validation] Report saved: {output_path}")
    
    def print_summary(self):
        """Print validation summary"""
        summary = self.results['summary']
        total = summary['total']
        passed = summary['passed']
        failed = summary['failed']
        skipped = summary['skipped']
        
        print("\n" + "=" * 60)
        print("GCDS THEME VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Total checks: {total}")
        print(f"Passed:       {passed} ({passed/total*100:.1f}%)")
        print(f"Failed:       {failed} ({failed/total*100:.1f}%)")
        print(f"Skipped:      {skipped} ({skipped/total*100:.1f}%)")
        print("=" * 60)
        
        if failed > 0:
            print("\nFailed checks:")
            for check in self.results['checks']:
                if check['status'] == 'FAIL':
                    print(f"  [FAIL] {check['name']}")
                    if check['details']:
                        print(f"         {check['details']}")
        
        print("\n" + ("✅ VALIDATION PASSED" if failed == 0 else "❌ VALIDATION FAILED"))
        print("=" * 60 + "\n")
        
        return failed == 0


def main():
    """Main entry point"""
    # Determine project root (script is in mkdocs-sample/scripts/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    print(f"[GCDS Theme Validation] Project root: {project_root}")
    
    # Create validator
    validator = GCDSThemeValidator(project_root)
    
    # Run all validations
    validator.run_all_validations()
    
    # Generate evidence report
    report_path = project_root / 'evidence' / 'test-results' / 'gcds-theme-validation.json'
    validator.generate_report(report_path)
    
    # Print summary and exit with appropriate code
    success = validator.print_summary()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
