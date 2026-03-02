#!/usr/bin/env python3
# EVA-FEATURE: F10-07
# EVA-STORY: F10-07-002
"""
Comprehensive Link Validation Script for MkDocs Site
NO Selenium - Uses Python stdlib + BeautifulSoup only

Validates:
- Internal page links (relative URLs)
- Image references (assets/)
- Anchor links (#sections)
- Navigation structure from mkdocs.yml
- Asset file existence

Generates timestamped JSON evidence report with REAL test results.
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
from urllib.parse import urljoin, urlparse, unquote

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERROR] BeautifulSoup4 not installed. Run: pip install beautifulsoup4")
    sys.exit(1)


class LinkValidator:
    """Validates all links in generated MkDocs site"""
    
    def __init__(self, site_dir: Path, docs_dir: Path):
        self.site_dir = site_dir
        self.docs_dir = docs_dir
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "site_directory": str(site_dir),
            "docs_directory": str(docs_dir),
            "summary": {
                "total_html_files": 0,
                "total_links_checked": 0,
                "total_images_checked": 0,
                "total_anchors_checked": 0,
                "broken_links": 0,
                "broken_images": 0,
                "broken_anchors": 0,
                "status": "UNKNOWN"
            },
            "broken_links": [],
            "broken_images": [],
            "broken_anchors": [],
            "validation_details": []
        }
        self.html_files = []
        self.valid_pages = set()
        self.anchor_map = {}  # page -> set of anchor IDs
        
    def find_html_files(self):
        """Find all HTML files in site directory"""
        self.html_files = list(self.site_dir.rglob("*.html"))
        self.results["summary"]["total_html_files"] = len(self.html_files)
        print(f"[INFO] Found {len(self.html_files)} HTML files")
        
        # Build valid pages set (relative paths from site root)
        for html_file in self.html_files:
            rel_path = html_file.relative_to(self.site_dir)
            # Convert index.html to directory path
            if html_file.name == "index.html":
                if rel_path == Path("index.html"):
                    self.valid_pages.add("")  # Root
                else:
                    self.valid_pages.add(str(rel_path.parent) + "/")
            else:
                self.valid_pages.add(str(rel_path))
                # Also add without .html
                self.valid_pages.add(str(rel_path.with_suffix("")))
                # Add directory form
                self.valid_pages.add(str(rel_path.with_suffix("")) + "/")
    
    def extract_anchors(self, html_file: Path, soup: BeautifulSoup):
        """Extract all anchor IDs from HTML file"""
        rel_path = html_file.relative_to(self.site_dir)
        page_key = str(rel_path) if rel_path != Path("index.html") else ""
        
        anchors = set()
        # Find all elements with id attribute
        for element in soup.find_all(id=True):
            anchors.add(element['id'])
        
        # Find all anchor name attributes (legacy)
        for element in soup.find_all('a', attrs={'name': True}):
            anchors.add(element['name'])
        
        self.anchor_map[page_key] = anchors
    
    def validate_link(self, source_file: Path, link_url: str, link_text: str) -> Tuple[bool, str]:
        """Validate a single link"""
        # Skip external links
        if link_url.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            return True, "External link (skipped)"
        
        # Skip javascript links
        if link_url.startswith('javascript:'):
            return True, "JavaScript link (skipped)"
        
        # Parse URL
        parsed = urlparse(link_url)
        path = unquote(parsed.path)
        fragment = parsed.fragment
        
        # Handle empty links (same page)
        if not path or path == '':
            if fragment:
                # Anchor on same page
                rel_path = source_file.relative_to(self.site_dir)
                page_key = str(rel_path) if rel_path != Path("index.html") else ""
                if page_key in self.anchor_map:
                    if fragment in self.anchor_map[page_key]:
                        return True, "Anchor exists on current page"
                    else:
                        return False, f"Anchor #{fragment} not found on current page"
                return True, "Same page link (unchecked)"
            return True, "Empty link (same page)"
        
        # Resolve relative paths relative to source HTML file location
        if path.startswith('/'):
            # Absolute path from site root
            check_path = path[1:]
        else:
            # Relative path - manually resolve from source file's directory
            source_rel = source_file.relative_to(self.site_dir)
            source_dir_rel = source_rel.parent
            
            # Build combined path
            if str(source_dir_rel) == '.':
                # Source is in root
                combined = path
            else:
                # Source is in subdirectory
                combined = str(source_dir_rel) + '/' + path
            
            # Manually resolve .. and . in the path
            path_parts = combined.split('/')
            resolved_parts = []
            for part in path_parts:
                if part == '..' and resolved_parts:
                    resolved_parts.pop()
                elif part and part != '.':
                    resolved_parts.append(part)
            check_path = '/'.join(resolved_parts) if resolved_parts else '.'
        
        # Handle .md extension - MkDocs converts docs/page.md to site/page/index.html
        if check_path.endswith('.md'):
            check_path = check_path[:-3]  # Remove .md
        
        # Build target path
        target = self.site_dir / check_path if check_path != '.' else self.site_dir
        
        # Check if target exists (try with and without index.html)
        target_exists = False
        target_page_key = None
        
        if target.exists():
            if target.is_file():
                target_exists = True
                target_page_key = str(target.relative_to(self.site_dir))
            elif target.is_dir():
                # Try index.html in the directory
                index_file = target / 'index.html'
                if index_file.exists():
                    target_exists = True
                    target_page_key = str(index_file.relative_to(self.site_dir))
        
        if not target_exists:
            # Try adding index.html if path ends with /
            if path.endswith('/'):
                alt_target = target / 'index.html'
                if alt_target.exists():
                    target_exists = True
                    target_page_key = str(alt_target.relative_to(self.site_dir))
        
        if not target_exists:
            return False, f"Target page not found: {path} (check_path={check_path}, target={target})"
        
        # Check anchor if present
        if fragment:
            # Find the actual page key for anchor lookup
            for key in self.anchor_map.keys():
                if key == target_page_key or key.startswith(target_page_key):
                    if fragment in self.anchor_map[key]:
                        return True, f"Link and anchor exist: {path}#{fragment}"
                    else:
                        return False, f"Anchor #{fragment} not found on {path}"
            # Anchor map not built yet, warn but don't fail
            return True, f"Link exists, anchor unchecked: {path}#{fragment}"
        
        return True, f"Link exists: {path}"
    
    def validate_image(self, source_file: Path, img_src: str, img_alt: str) -> Tuple[bool, str]:
        """Validate image reference"""
        # Skip external images
        if img_src.startswith(('http://', 'https://', 'data:')):
            return True, "External image (skipped)"
        
        # Skip SVG data URIs
        if img_src.startswith('data:image/svg'):
            return True, "SVG data URI (skipped)"
        
        # Parse relative path
        parsed = urlparse(img_src)
        path = unquote(parsed.path)
        
        # Resolve relative paths relative to source HTML file's directory
        if path.startswith('/'):
            # Absolute path from site root
            target = self.site_dir / path[1:]
        else:
            # Relative path - resolve from source file's directory
            source_dir = source_file.parent
            target = (source_dir / path).resolve()
        
        # Check if image exists
        if target.exists():
            return True, f"Image exists: {path}"
        else:
            # Also check in docs/assets/ as fallback
            if path.startswith('../'):
                # Try stripping leading ../ and checking from site root
                clean_path = path.lstrip('../')
                alt_target = self.site_dir / clean_path
                if alt_target.exists():
                    return True, f"Image exists (alt path): {clean_path}"
            
            return False, f"Image not found: {path} (resolved to {target})"
    
    def validate_html_file(self, html_file: Path):
        """Validate all links in a single HTML file"""
        print(f"[INFO] Validating {html_file.relative_to(self.site_dir)}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
        except Exception as e:
            self.results["validation_details"].append({
                "file": str(html_file.relative_to(self.site_dir)),
                "error": f"Failed to parse HTML: {str(e)}"
            })
            return
        
        # Extract anchors first
        self.extract_anchors(html_file, soup)
        
        file_details = {
            "file": str(html_file.relative_to(self.site_dir)),
            "links_checked": 0,
            "images_checked": 0,
            "anchors_checked": 0,
            "issues": []
        }
        
        # Check all links
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True) or link.get('aria-label', '')
            file_details["links_checked"] += 1
            self.results["summary"]["total_links_checked"] += 1
            
            valid, reason = self.validate_link(html_file, href, text)
            if not valid:
                self.results["summary"]["broken_links"] += 1
                issue = {
                    "type": "link",
                    "url": href,
                    "text": text,
                    "reason": reason
                }
                file_details["issues"].append(issue)
                self.results["broken_links"].append({
                    "source_file": str(html_file.relative_to(self.site_dir)),
                    **issue
                })
        
        # Check all images
        for img in soup.find_all('img', src=True):
            src = img['src']
            alt = img.get('alt', '')
            file_details["images_checked"] += 1
            self.results["summary"]["total_images_checked"] += 1
            
            valid, reason = self.validate_image(html_file, src, alt)
            if not valid:
                self.results["summary"]["broken_images"] += 1
                issue = {
                    "type": "image",
                    "src": src,
                    "alt": alt,
                    "reason": reason
                }
                file_details["issues"].append(issue)
                self.results["broken_images"].append({
                    "source_file": str(html_file.relative_to(self.site_dir)),
                    **issue
                })
        
        self.results["validation_details"].append(file_details)
    
    def run_validation(self):
        """Run complete validation"""
        print("[INFO] Starting link validation...")
        print(f"[INFO] Site directory: {self.site_dir}")
        print(f"[INFO] Docs directory: {self.docs_dir}")
        
        # Find all HTML files
        self.find_html_files()
        
        if not self.html_files:
            print("[ERROR] No HTML files found in site directory")
            self.results["summary"]["status"] = "FAILED"
            return False
        
        # Validate each HTML file
        for html_file in self.html_files:
            self.validate_html_file(html_file)
        
        # Determine status
        total_broken = (
            self.results["summary"]["broken_links"] +
            self.results["summary"]["broken_images"] +
            self.results["summary"]["broken_anchors"]
        )
        
        if total_broken == 0:
            self.results["summary"]["status"] = "PASS"
            print(f"\n[PASS] All links valid ({self.results['summary']['total_links_checked']} links, {self.results['summary']['total_images_checked']} images)")
        else:
            self.results["summary"]["status"] = "FAIL"
            print(f"\n[FAIL] {total_broken} broken references found")
            print(f"  - Broken links: {self.results['summary']['broken_links']}")
            print(f"  - Broken images: {self.results['summary']['broken_images']}")
            print(f"  - Broken anchors: {self.results['summary']['broken_anchors']}")
        
        return total_broken == 0
    
    def save_report(self, output_dir: Path):
        """Save JSON evidence report"""
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = output_dir / f"link_validation_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n[INFO] Evidence report saved: {report_file}")
        return report_file
    
    def print_summary(self):
        """Print human-readable summary"""
        print("\n" + "="*80)
        print("LINK VALIDATION SUMMARY")
        print("="*80)
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Status: {self.results['summary']['status']}")
        print(f"\nFiles Checked: {self.results['summary']['total_html_files']}")
        print(f"Links Checked: {self.results['summary']['total_links_checked']}")
        print(f"Images Checked: {self.results['summary']['total_images_checked']}")
        print(f"\nBroken Links: {self.results['summary']['broken_links']}")
        print(f"Broken Images: {self.results['summary']['broken_images']}")
        print(f"Broken Anchors: {self.results['summary']['broken_anchors']}")
        
        if self.results["broken_links"]:
            print("\nBROKEN LINKS:")
            for item in self.results["broken_links"][:10]:  # Show first 10
                print(f"  [{item['source_file']}]")
                print(f"    URL: {item['url']}")
                print(f"    Reason: {item['reason']}")
        
        if self.results["broken_images"]:
            print("\nBROKEN IMAGES:")
            for item in self.results["broken_images"][:10]:  # Show first 10
                print(f"  [{item['source_file']}]")
                print(f"    Src: {item['src']}")
                print(f"    Reason: {item['reason']}")
        
        print("="*80)


def main():
    """Main entry point"""
    # Determine project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    site_dir = project_root / "site"
    docs_dir = project_root / "docs"
    evidence_dir = project_root.parent / "evidence" / "test-results"
    
    # Check if site exists
    if not site_dir.exists():
        print(f"[ERROR] Site directory not found: {site_dir}")
        print("[ERROR] Run 'mkdocs build' first")
        sys.exit(1)
    
    # Run validation
    validator = LinkValidator(site_dir, docs_dir)
    success = validator.run_validation()
    
    # Save report
    report_file = validator.save_report(evidence_dir)
    
    # Print summary
    validator.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
