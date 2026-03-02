"""
Evidence Collector Component
=============================
Collect debug artifacts for troubleshooting and validation.
Windows Enterprise Encoding Safe: ASCII-only output.
"""

import json
import traceback
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


class EvidenceCollector:
    """Collect debug artifacts and evidence for MkDocs PoC"""
    
    def __init__(self, component_name: str):
        self.component_name = component_name
        self.base_path = Path(__file__).parent.parent.parent
        
        # Standard EVA directories
        self.debug_path = self.base_path / "debug"
        self.evidence_path = self.base_path / "evidence"
        self.logs_path = self.base_path / "logs"
        
        # Ensure directories exist
        for path in [self.debug_path, self.evidence_path, self.logs_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def capture_state(self, context: str, additional_data: Optional[Dict[str, Any]] = None):
        """Capture debug state for troubleshooting"""
        debug_file = self.debug_path / f"{self.component_name}_{context}_{self.timestamp}.json"
        
        state = {
            "component": self.component_name,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "cwd": str(Path.cwd()),
            "project_root": str(self.base_path)
        }
        
        if additional_data:
            state["additional_data"] = additional_data
        
        with open(debug_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
        
        print(f"[INFO] Debug state captured: {debug_file.name}")
    
    def log_error(self, operation_name: str, error: Exception):
        """Log structured error with full context"""
        log_file = self.logs_path / f"{self.component_name}_errors_{datetime.now().strftime('%Y%m%d')}.log"
        
        error_entry = f"""
{'='*80}
[ERROR] {datetime.now().isoformat()}
Operation: {operation_name}
Component: {self.component_name}
Error Type: {type(error).__name__}
Error Message: {str(error)}
{'='*80}
Traceback:
{traceback.format_exc()}
{'='*80}

"""
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(error_entry)
        
        print(f"[INFO] Error logged to: {log_file.name}")
    
    def save_evidence(self, evidence_type: str, data: Dict[str, Any]):
        """Save evidence artifact for validation"""
        evidence_dir = self.evidence_path / "test-results"
        evidence_dir.mkdir(parents=True, exist_ok=True)
        
        evidence_file = evidence_dir / f"{evidence_type}_{self.timestamp}.json"
        
        evidence_data = {
            "evidence_type": evidence_type,
            "component": self.component_name,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        with open(evidence_file, 'w', encoding='utf-8') as f:
            json.dump(evidence_data, f, indent=2)
        
        print(f"[INFO] Evidence saved: {evidence_file.name}")
        return evidence_file
