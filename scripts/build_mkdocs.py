# EVA-FEATURE: F10-07
# EVA-STORY: F10-07-001
"""
MkDocs PoC - Professional Builder
==================================
Zero-setup execution with professional component architecture.

Based on EVA Professional Component Architecture Standards (Project 06/07).
Windows Enterprise Encoding Safe: ASCII-only output.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime


def main():
    """Main entry point with professional runner pattern"""
    
    # Import components after path setup
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from scripts.components.mkdocs_generator import MkDocsGenerator
    from scripts.components.evidence_collector import EvidenceCollector
    from scripts.components.validation_reporter import ValidationReporter
    
    print("[INFO] MkDocs PoC - Professional Builder")
    print(f"[INFO] Started at: {datetime.now().isoformat()}")
    print()
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="MkDocs PoC Professional Builder"
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate MkDocs sample site structure"
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build MkDocs site to static HTML"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run full PoC (generate + build + validate)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean generated artifacts before building"
    )
    
    args = parser.parse_args()
    
    # Default to --all if no args provided
    if not (args.generate or args.build or args.all):
        args.all = True
    
    try:
        # Initialize components
        generator = MkDocsGenerator()
        evidence = EvidenceCollector("build_mkdocs")
        reporter = ValidationReporter()
        
        # Execute requested operations
        if args.clean or args.all:
            print("[INFO] Cleaning previous artifacts...")
            generator.clean_artifacts()
            print("[PASS] Clean complete")
            print()
        
        if args.generate or args.all:
            print("[INFO] Generating MkDocs sample site...")
            evidence.capture_state("generate_before")
            
            site_path = generator.generate_site()
            
            evidence.capture_state("generate_success")
            print(f"[PASS] Site generated at: {site_path}")
            print()
        
        if args.build or args.all:
            print("[INFO] Building MkDocs site to static HTML...")
            evidence.capture_state("build_before")
            
            output_path = generator.build_site()
            
            evidence.capture_state("build_success")
            print(f"[PASS] Static HTML built at: {output_path}")
            print()
        
        if args.all:
            print("[INFO] Generating validation checklist...")
            reporter.generate_quick_validation_report()
            print("[PASS] Validation checklist generated")
            print()
        
        # Final summary
        print("[INFO] ============================================")
        print("[PASS] MkDocs PoC build completed successfully")
        print("[INFO] ============================================")
        print()
        print("[INFO] Generated artifacts:")
        print(f"[INFO]   - MkDocs source: {generator.mkdocs_sample_path / 'docs'}")
        print(f"[INFO]   - Static HTML: {generator.mkdocs_sample_path / 'site'}")
        print(f"[INFO]   - Debug artifacts: {generator.base_path / 'debug'}")
        print(f"[INFO]   - Evidence: {generator.base_path / 'evidence'}")
        print()
        print("[INFO] Next steps:")
        print("[INFO]   1. Review VALIDATION-CHECKLIST.md for test procedures")
        print("[INFO]   2. Upload 'mkdocs-sample/site/' to SharePoint Online")
        print("[INFO]   3. Deploy 'mkdocs-sample/site/' to Azure Static Website")
        print("[INFO]   4. Complete validation checklist for both platforms")
        print()
        
        return 0
        
    except Exception as e:
        print()
        print(f"[ERROR] Build failed: {str(e)}")
        print(f"[INFO] Check logs/ directory for details")
        evidence.capture_state("build_error")
        evidence.log_error("build_mkdocs", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
