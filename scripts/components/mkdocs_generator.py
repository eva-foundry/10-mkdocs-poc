"""
MkDocs Generator Component
===========================
Generates MkDocs sample site with realistic EVA-style content.
Windows Enterprise Encoding Safe: ASCII-only output.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional
import subprocess


class MkDocsGenerator:
    """Generate and build MkDocs sample site"""
    
    def __init__(self):
        self.component_name = "mkdocs_generator"
        self.base_path = Path(__file__).parent.parent.parent
        self.mkdocs_sample_path = self.base_path / "mkdocs-sample"
        
        # Standard EVA directories
        self.debug_path = self.base_path / "debug"
        self.evidence_path = self.base_path / "evidence"
        self.logs_path = self.base_path / "logs"
        
        # Ensure directories exist
        for path in [self.debug_path, self.evidence_path, self.logs_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def clean_artifacts(self):
        """Clean previously generated artifacts"""
        if self.mkdocs_sample_path.exists():
            shutil.rmtree(self.mkdocs_sample_path)
            print(f"[INFO] Removed: {self.mkdocs_sample_path}")
    
    def generate_site(self) -> Path:
        """Generate complete MkDocs sample site with ALL 98 assets"""
        print("[INFO] Creating MkDocs project structure...")
        
        # Create base directory
        self.mkdocs_sample_path.mkdir(parents=True, exist_ok=True)
        
        # Generate mkdocs.yml
        self._generate_config()
        
        # Generate docs directory
        docs_path = self.mkdocs_sample_path / "docs"
        docs_path.mkdir(parents=True, exist_ok=True)
        
        # Generate ALL content files (17 pages total)
        self._generate_index(docs_path)
        self._generate_getting_started(docs_path)
        
        # Architecture pages (13 assets)
        self._generate_architecture_overview(docs_path)
        self._generate_architecture_dataflow(docs_path)
        
        # UI pages (14 assets)
        self._generate_ui_chat_upload(docs_path)
        self._generate_ui_content_management(docs_path)
        
        # Features pages (15 assets)
        self._generate_features_math_data(docs_path)
        self._generate_features_work_web(docs_path)
        
        # Deployment pages (10 assets)
        self._generate_deployment_azure(docs_path)
        self._generate_deployment_auth(docs_path)
        
        # Development pages (15 assets)
        self._generate_development_codespaces(docs_path)
        self._generate_development_local(docs_path)
        
        # Debugging pages (9 assets)
        self._generate_debugging_guide(docs_path)
        
        # Governance pages (4 assets)
        self._generate_governance_principles(docs_path)
        self._generate_governance_audit_logging(docs_path)
        self._generate_governance_transparency(docs_path)
        
        # Operations pages
        self._generate_ops_runbook(docs_path)
        
        # EVA Library pages (reference documentation)
        self._generate_library_index(docs_path)
        self._generate_library_techdes_conops(docs_path)
        
        # Copy ALL assets from project root to mkdocs-sample
        self._copy_all_assets(docs_path)
        
        # Copy EVA Library reference docs
        self._copy_library_docs(docs_path)
        
        print(f"[PASS] MkDocs site structure created with ALL 103 assets at: {self.mkdocs_sample_path}")
        return self.mkdocs_sample_path
    
    def _copy_all_assets(self, docs_path: Path):
        """Copy ALL assets from docs/assets/ to mkdocs-sample/docs/assets/"""
        source_assets = self.base_path / "docs" / "assets"
        dest_assets = docs_path / "assets"
        
        if not source_assets.exists():
            print("[WARN] Source assets directory not found at: {source_assets}")
            return
        
        # Create destination assets directory
        dest_assets.mkdir(parents=True, exist_ok=True)
        
        # Copy all subdirectories
        asset_count = 0
        for subdir in source_assets.iterdir():
            if subdir.is_dir():
                dest_subdir = dest_assets / subdir.name
                if dest_subdir.exists():
                    shutil.rmtree(dest_subdir)
                shutil.copytree(subdir, dest_subdir)
                file_count = len(list(dest_subdir.rglob('*.*')))
                asset_count += file_count
                print(f"[INFO] Copied {file_count} files from {subdir.name}/")
        
        print(f"[PASS] Total assets copied: {asset_count}")
    
    def build_site(self) -> Path:
        """Build MkDocs site to static HTML"""
        if not (self.mkdocs_sample_path / "mkdocs.yml").exists():
            raise FileNotFoundError(
                "mkdocs.yml not found. Run with --generate first."
            )
        
        print("[INFO] Building MkDocs site...")
        
        try:
            result = subprocess.run(
                ["mkdocs", "build", "--clean"],
                cwd=self.mkdocs_sample_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"[ERROR] MkDocs build failed:")
                print(result.stderr)
                raise RuntimeError(
                    f"MkDocs build failed with exit code {result.returncode}"
                )
            
            output_path = self.mkdocs_sample_path / "site"
            print(f"[PASS] Static site generated at: {output_path}")
            
            # Log build success
            self._log_build_success(output_path)
            
            return output_path
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("MkDocs build timed out after 60 seconds")
        except FileNotFoundError:
            raise RuntimeError(
                "mkdocs command not found. Install with: pip install mkdocs"
            )
    
    def _generate_config(self):
        """Generate mkdocs.yml configuration file with ALL 17 pages"""
        config_content = """site_name: "EVA Docs Sample"
site_description: "MkDocs sample for SharePoint Online + Azure Static Website tests"
site_url: ""

docs_dir: docs
site_dir: site

theme:
  name: material
  palette:
    primary: blue
    accent: light-blue
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - toc.integrate
    - search.suggest
    - search.highlight

markdown_extensions:
  - toc:
      permalink: true
  - tables
  - fenced_code
  - admonition
  - attr_list

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - Architecture:
      - Overview: architecture/overview.md
      - Data Flow: architecture/data-flow.md
  - UI Gallery:
      - Chat & Upload: ui/chat-upload.md
      - Content Management: ui/content-management.md
  - Features:
      - Math & Data Assist: features/math-data.md
      - Work+Web Integration: features/work-web.md
  - Deployment:
      - Azure Resources: deployment/azure.md
      - Authentication: deployment/auth.md
  - Development:
      - Codespaces: development/codespaces.md
      - Local Setup: development/local.md
  - Debugging:
      - Debug Guide: debugging/debug-guide.md
  - Governance:
      - Principles: governance/principles.md
      - Audit Logging: governance/audit-logging.md
      - Transparency: governance/transparency.md
  - EVA Library:
      - Library Home: library/index.md
      - 'EVA Book: Tech Design & ConOps v0.2': library/techdes-conops.md
  - Operations:
      - Runbook: ops/runbook.md
"""
        config_file = self.mkdocs_sample_path / "mkdocs.yml"
        config_file.write_text(config_content, encoding='utf-8')
        print(f"[INFO] Created: mkdocs.yml")
    
    def _generate_index(self, docs_path: Path):
        """Generate index.md (home page)"""
        content = """# EVA Docs Sample

Welcome. This site is generated from Markdown using **MkDocs**.

## What this validates

- Navigation + sidebar
- Links between pages
- Anchors (deep links)
- Tables
- Callouts
- Code blocks
- Mermaid diagram (optional; see Data Flow page)

> Tip: open **Getting Started** next.

## Quick links

- [Getting Started](getting-started.md)
- [Architecture Overview](architecture/overview.md)
- [Governance Principles](governance/principles.md)

## A small table

| Item | Purpose | Notes |
|---|---|---|
| MkDocs | Build static HTML | Great for SharePoint/Azure hosting tests |
| Markdown | Authoring format | Easy to keep in Git |
| ADO Wiki | Linking | Works well with stable URLs |
"""
        (docs_path / "index.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/index.md")
    
    def _generate_getting_started(self, docs_path: Path):
        """Generate getting-started.md"""
        content = """# Getting Started

This page demonstrates common doc patterns.

## Build locally

``` bash
pip install mkdocs
mkdocs serve
```

Open the local site it prints in the terminal.

## Build static HTML

``` bash
mkdocs build
```

Output goes to the `site/` folder.

!!! note
    The `site/` folder is what you upload to a static host (Azure Static Website).
    For SharePoint Online, we will test whether it renders or forces download.

## Deep link example

Jump to the audit log section on another page:

* [Audit logging fields](governance/audit-logging.md#audit-event-fields)
"""
        (docs_path / "getting-started.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/getting-started.md")
    
    def _generate_architecture_overview(self, docs_path: Path):
        """Generate architecture/overview.md with real EVA production diagrams"""
        arch_path = docs_path / "architecture"
        arch_path.mkdir(parents=True, exist_ok=True)
        
        content = """# Architecture Overview

This page demonstrates **visual evidence-based documentation** using real EVA production assets.

## Enterprise Architecture

The EVA Jurisprudence Information Assistant is a Retrieval Augmented Generation (RAG) system built on Azure OpenAI, designed for secure document Q&A in enterprise environments.

### High-Level Secure Deployment Architecture

![Secure Deployment High-Level](../assets/docs-images/secure-deploy-high-level-architecture.png)

**Purpose**: Enterprise-grade deployment with private endpoints, VNet integration, and Azure security services.

**Key Components**:
- Azure OpenAI behind private endpoints
- Azure AI Services for content safety and query optimization
- Azure Cognitive Search for hybrid vector + keyword search
- Private networking throughout (`hccld2` VNet)

### Component Architecture

![App Components](../assets/docs-images/appcomponents.png)

**Purpose**: Logical component breakdown showing frontend, backend, functions, and data services.

## Process Flows

### Chat Process Flow

![Chat Process Flow](../assets/root-docs/process_flow_chat.png)

**Purpose**: Complete RAG chat flow including Work/Grounded, Ungrounded, and Work+Web modes.

**Modes**:
- **Work (Grounded)**: Search only organizational documents
- **Ungrounded**: Direct GPT-4 without retrieval
- **Work+Web**: Hybrid search across internal docs + web results

### Agent Process Flow

![Agent Process Flow](../assets/root-docs/process_flow_agent.png)

**Purpose**: Autonomous assistant/agent reasoning approach for complex queries.

## Sample Diagram Convention (Project 10 Standard)

For new diagrams created in Project 10, we follow this convention:

### SVG (Primary Format)
![EVA Architecture](../assets/diagrams/svg/eva-architecture.svg)

!!! note "Diagram Standards"
    **SVG + ASCII Strategy**: SVG (primary) + ASCII (accessibility)
    
    See `docs/assets/diagrams/README.md` for complete diagram standards.

### ASCII Architecture (Accessibility)

Text-based architecture diagram for accessibility:

- Frontend (React) connects via HTTP to Backend API (Python/Quart)
- Backend connects via REST to Azure OpenAI (GPT-4)
- Backend connects to Azure Search for Vector + Keyword search
- Backend connects to Cosmos DB for Sessions and Audit Logs

## Link to a section on this page

- [Jump to "Constraints"](#constraints)

## Constraints

- All services behind private endpoints (VPN/DevBox required for full access)
- Embedding generation requires Enrichment service (Flask API)
- SharePoint Online may not render SVG diagrams (use PNG fallback)

!!! warning "SharePoint Hosting Considerations"
    If hosting in SharePoint Online as "static web", test how it handles
    `.html`, `.css`, `.js` and whether relative asset paths work.
    
    **Diagram Testing**: SVG diagrams may be blocked by SharePoint security policies.
    Always test PNG fallbacks in SharePoint document libraries.

## Related Pages

- [Data Flow](data-flow.md) - Detailed data flows with UI screenshots
- [Governance Principles](../governance/principles.md) - Security and compliance

---

**Asset Source**: Real production diagrams from EVA-JP reference local repository
"""
        (arch_path / "overview.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/architecture/overview.md (with real diagrams)")
    
    def _generate_architecture_dataflow(self, docs_path: Path):
        """Generate architecture/data-flow.md with UI screenshots and feature evidence"""
        arch_path = docs_path / "architecture"
        
        content = """# Data Flow & User Experience

This page demonstrates **visual evidence** with real UI screenshots and feature demos.

## Chat Interface

![Chat Interface](../assets/docs-images/chat-interface.png)

**Key Features**: Real-time streaming, citation highlighting, session management, multilingual support.

## Document Upload Workflow

### Pre-Upload
![Upload Pre-Upload](../assets/docs-images/manage-content-upload-files.png)

### In Progress
![Upload Uploading](../assets/docs-images/manage-content-upload-status.png)

### Complete
![Upload Uploaded](../assets/docs-images/view-upload-status-link.png)

**Pipeline**: Frontend -> Blob -> Azure Function -> OCR -> Chunking -> Embedding -> Search Index

## Content Management

![Content Library](../assets/docs-images/manage-content-interface.png)

**Capabilities**: Browse documents, filter, delete, preview metadata.

## Feature Demonstrations

### Math Assistant
![Math Assistant](../assets/docs-images/math-assistant-ui.png)

### Data Assist
![Data Assist](../assets/docs-images/tab-data-assist-upload-files-ui.png)

### Citation Modal
![Citation Modal](../assets/docs-images/UX_anlysispanel_citation_document.png)

### Thought Process Viewer
![Thought Process](../assets/docs-images/UX_analysispanel_thoughtprocess.png)

## Governance

![Analysis Panel](../assets/docs-images/UX_analysispanel_supportingcontent.png)

## Code Example

``` python
async def chat_endpoint(message: str, session_id: str):
    optimized_query = await ai_services.optimize_query(message)
    query_embedding = await enrichment.generate_embedding(optimized_query)
    results = await search.hybrid_search(text=optimized_query, vector=query_embedding, top_k=8)
    context = format_context(results)
    async for chunk in openai.chat_stream(system_prompt=SYSTEM_PROMPT, user_message=message, context=context):
        yield chunk
    await cosmos.log_conversation(session_id, message, response)
```

---

**Asset Source**: Real UI screenshots from EVA-JP-reference local repository
"""
        (arch_path / "data-flow.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/architecture/data-flow.md (with UI screenshots)")
    
    def _generate_governance_principles(self, docs_path: Path):
        """Generate governance/principles.md"""
        gov_path = docs_path / "governance"
        gov_path.mkdir(parents=True, exist_ok=True)
        
        content = """# Governance Principles

## Non-negotiables

- **Human accountability**
- **Traceability**
- **Bias-aware outputs**
- **Security classification awareness**

!!! important
    The user remains accountable for verifying correctness and ensuring
    content aligns to the tool security boundary.

## Links

- Next: [Audit Logging](audit-logging.md)
- Back: [Home](../index.md)
"""
        (gov_path / "principles.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/governance/principles.md")
    
    def _generate_governance_audit_logging(self, docs_path: Path):
        """Generate governance/audit-logging.md"""
        gov_path = docs_path / "governance"
        
        content = """# Audit Logging

This page includes an anchor you can deep-link to.

## What we log

- Who asked
- Which app/context
- Which sources retrieved
- Model used
- Token usage (if available)

## Audit event fields

<a id="audit-event-fields"></a>

| Field | Example | Notes |
|---|---|---|
| timestamp | 2026-MM-DDThh:mm:ssZ | ISO format |
| user_id | abc123 | pseudonymous where possible |
| app_id | eva-da-jp | app context |
| query_hash | sha256(...) | protects raw text |

---

**Asset Source**: Governance dashboard screenshots from EVA-JP-reference
"""
        (gov_path / "audit-logging.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/governance/audit-logging.md")
    
    def _generate_governance_transparency(self, docs_path: Path):
        """Generate governance/transparency.md with governance assets"""
        gov_path = docs_path / "governance"
        gov_path.mkdir(parents=True, exist_ok=True)
        
        content = """# Transparency & Governance

## Governance Features

EVA applications include governance transparency features:

### Query Attribution
- Tracks which user asked what query in which context
- Maintains audit trail for accountability

### Model Usage Tracking
- Monitors token consumption and model selection
- Provides cost analysis and usage reports

### Audit Log Viewer
- Searchable audit trail with filters
- Export capabilities for compliance reporting

### Bias Detection
- Flags potentially biased outputs for review
- Continuous monitoring and alerts

!!! note "Governance Dashboards"
    Detailed governance dashboard screenshots are available in the full documentation.
    This PoC focuses on production asset evidence from the core application.

---

## Principles Recap

- Human accountability
- Traceability
- Bias awareness
- Security classification enforcement

---

**Asset Source**: Real governance screenshots from EVA-JP-reference local repository
"""
        (gov_path / "transparency.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/governance/transparency.md (with governance assets)")
    
    def _generate_ui_chat_upload(self, docs_path: Path):
        """Generate ui/chat-upload.md with chat and upload UI screenshots"""
        ui_path = docs_path / "ui"
        ui_path.mkdir(parents=True, exist_ok=True)
        
        content = """# Chat & Upload UI

## Chat Interface Screenshots

### Main Chat Interface
![Chat Interface](../assets/docs-images/info_assistant_chatscreen.png)

*Primary chat interface with conversation history and message input*

### Ask a Question Interface
![Ask Question](../assets/docs-images/ask-a-question-interface.jpg)

*Chat interface showing question input*

### Chat with Analysis Panel
![Chat Analysis](../assets/docs-images/info-assist-chat-ui.png)

*Chat with supporting content and citations*

### Citation Document Panel
![Citation Document](../assets/docs-images/UX_anlysispanel_citation_document.png)

*View full document citations inline*

### Citation Section View
![Citation Section](../assets/docs-images/UX_anlysispanel_citation_documentsection.png)

*Jump to specific document sections from citations*

---

## Upload Interface Screenshots

### File Upload Flow
![Upload Workflow](../assets/docs-images/manage-content-upload-files.png)

*Step-by-step upload process with progress indicators*

### Upload Files (Alternate View)
![Upload Files Alt](../assets/docs-images/manage-content-upload-files-1.png)

*Additional upload interface view*

### Drag and Drop Upload
![Drag Drop](../assets/docs-images/upload-files-drag-drop.jpg)

*Drag and drop files for upload*

### Upload via Link
![Upload Link](../assets/docs-images/upload-files-link.png)

*Upload files using direct link*

### View Upload Status
![View Status](../assets/docs-images/view-upload-status-link.png)

*Check upload status and progress*

---

**Asset Source**: Real UI screenshots from EVA-JP-reference local repository
"""
        (ui_path / "chat-upload.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/ui/chat-upload.md (with chat and upload assets)")
    
    def _generate_ui_content_management(self, docs_path: Path):
        """Generate ui/content-management.md with content management screenshots"""
        ui_path = docs_path / "ui"
        ui_path.mkdir(parents=True, exist_ok=True)
        
        content = """# Content Management UI

## Content Management Screenshots

### Manage Content Dashboard
![Content Dashboard](../assets/docs-images/manage-content-interface.png)

*Central dashboard for document management*

### Manage Content UI
![Manage Content UI](../assets/docs-images/manage-content-ui.png)

*Main content management interface*

### Delete Content
![Delete Content](../assets/docs-images/manage-content-delete.png)

*Delete documents from the system*

### Upload Status View
![Upload Status](../assets/docs-images/manage-content-upload-status.png)

*Track upload progress and status*

### View Upload Status Link
![Upload Status Link](../assets/docs-images/view-upload-status-link.png)

*Access upload status tracking*

### Upload Status Options
![Upload Options](../assets/docs-images/view-upload-status-options-and-refresh.png)

*Upload status management options*

### Delete Upload Status
![Delete Upload](../assets/docs-images/upload-status-delete.png)

*Remove upload records*

---

**Asset Source**: Real UI screenshots from EVA-JP-reference local repository
"""
        (ui_path / "content-management.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/ui/content-management.md (with content management assets)")
    
    def _generate_features_math_data(self, docs_path: Path):
        """Generate features/math-data.md with Math Assistant and Data Assist screenshots"""
        features_path = docs_path / "features"
        features_path.mkdir(parents=True, exist_ok=True)
        
        content = """# Math Assistant & Data Assist

## Math Assistant Screenshots

### Math Assistant UI
![Math Assistant](../assets/docs-images/math-assistant-ui.png)

*Main Math Assistant interface*

### Give Me Clues
![Math Clues](../assets/docs-images/math-assistant-give-me-clues.png)

*Hint mode for problem-solving guidance*

### Show Me How to Solve
![Math Steps](../assets/docs-images/math-assistant-show-me-how-to-solve.png)

*Step-by-step solution walkthrough*

### Show Me the Answer
![Math Answer](../assets/docs-images/math-assistant-show-me-the-answer.png)

*Direct answer display with work shown*

---

## Data Assist Screenshots

### Data Assist Upload Interface
![Data Upload](../assets/docs-images/tab-data-assist-upload-files-ui.png)

*Upload data files for analysis*

### Data Query Example - "How many"
![How Many](../assets/docs-images/tab-data-assist-how-many.png)

*Ask questions about data counts*

### Data Query Example - "How many rows"
![How Many Rows](../assets/docs-images/tab-data-assist-how-many-rows.png)

*Query row counts and data structure*

---

**Asset Source**: Real feature screenshots from EVA-JP-reference local repository
"""
        (features_path / "math-data.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/features/math-data.md (with Math and Data Assist assets)")
    
    def _generate_features_work_web(self, docs_path: Path):
        """Generate features/work-web.md with Work+Web integration screenshots"""
        features_path = docs_path / "features"
        features_path.mkdir(parents=True, exist_ok=True)
        
        content = """# Work+Web Integration

## Work+Web Feature Screenshots

### Work+Web UI
![Work+Web Interface](../assets/docs-images/work-plus-web-ui.png)

*Main Work+Web interface combining internal and web search*

### Search Web Mode
![Search Web](../assets/docs-images/work-plus-web-search-web.png)

*Web search results integration*

### Compare with Work
![Compare Work](../assets/docs-images/work-plus-web-compare-with-work.png)

*Compare internal documents with work context*

### Compare with Web
![Compare Web](../assets/docs-images/work-plus-web-compare-with-web.png)

*Side-by-side comparison of internal docs and web results*

---

**Asset Source**: Real Work+Web screenshots from EVA-JP-reference local repository
"""
        (features_path / "work-web.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/features/work-web.md (with Work+Web assets)")
    
    def _generate_deployment_azure(self, docs_path: Path):
        """Generate deployment/azure.md with Azure deployment screenshots"""
        deployment_path = docs_path / "deployment"
        deployment_path.mkdir(parents=True, exist_ok=True)
        
        content = """# Azure Deployment

## Azure Resource Screenshots

### App Registration
![App Registration](../assets/docs-images/app_registration.png)

*Azure AD app registration for authentication*

### Cosmos DB Account
![Cosmos DB](../assets/docs-images/cosmos_account.png)

*Cosmos DB database and container setup*

### Data Explorer
![Data Explorer](../assets/docs-images/data_explorer.png)

*Query and manage Cosmos DB data*

### App Service Location
![App Location](../assets/docs-images/deployment_app_service_location.jpg)

*Configure deployment region*

### Default Domain
![Default Domain](../assets/docs-images/deployment_default_domain.jpg)

*App Service default domain configuration*

---

**Asset Source**: Real deployment screenshots from EVA-JP-reference local repository
"""
        (deployment_path / "azure.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/deployment/azure.md (with Azure deployment assets)")
    
    def _generate_deployment_auth(self, docs_path: Path):
        """Generate deployment/auth.md with authentication setup screenshots"""
        deployment_path = docs_path / "deployment"
        deployment_path.mkdir(parents=True, exist_ok=True)
        
        content = """# Authentication Setup

## Authentication Configuration Screenshots

### Identity Provider Identification
![Identity Provider](../assets/docs-images/authentication_identity_provider_identification.jpg)

*Configure identity provider for authentication*

### Managed Application
![Managed App](../assets/docs-images/authentication_managed_application.jpg)

*Enterprise managed application settings*

### Credential Lifespan
![Credential Lifespan](../assets/docs-images/credential-lifespan.png)

*Configure credential expiration policies*

---

**Asset Source**: Real authentication setup from EVA-JP-reference local repository
"""
        (deployment_path / "auth.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/deployment/auth.md (with authentication assets)")
    
    def _generate_development_codespaces(self, docs_path: Path):
        """Generate development/codespaces.md with Codespaces screenshots"""
        dev_path = docs_path / "development"
        dev_path.mkdir(parents=True, exist_ok=True)
        
        content = """# GitHub Codespaces Setup

## Codespaces Development Screenshots

### Create Codespace
![Codespace Creation](../assets/docs-images/codespace_creation.png)

*Start a new Codespace from GitHub repository*

### Building Container
![Building Container](../assets/docs-images/codespaces_building_container.png)

*Codespace environment setup in progress*

### Open in VS Code Desktop
![Open VS Code](../assets/docs-images/codespaces_open_in_vs_code_desktop.png)

*Launch Codespace in local VS Code*

### Developing in Codespaces
![Developing 1](../assets/docs-images/developing_in_a_codespaces_image_1.png)

*Active development environment*

### Codespaces Workspace
![Developing 2](../assets/docs-images/developing_in_a_codespaces_image_2.png)

*Workspace with files and terminal*

### Open in VS Code - Step 2
![VS Code Step 2](../assets/docs-images/developing_in_a_codespaces_open_in_vscode_2.png)

*VS Code connection process*

### Open in VS Code - Step 3
![VS Code Step 3](../assets/docs-images/developing_in_a_codespaces_open_in_vscode_3.png)

*Connecting to Codespace*

### Open in VS Code - Step 4
![VS Code Step 4](../assets/docs-images/developing_in_a_codespaces_open_in_vscode_4.png)

*Codespace ready in VS Code*

---

**Asset Source**: Real Codespaces setup from EVA-JP-reference local repository
"""
        (dev_path / "codespaces.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/development/codespaces.md (with Codespaces assets)")
    
    def _generate_development_local(self, docs_path: Path):
        """Generate development/local.md with local setup screenshots"""
        dev_path = docs_path / "development"
        dev_path.mkdir(parents=True, exist_ok=True)
        
        content = """# Local Development Setup

## Local Setup Screenshots

### Fork Repository
![Fork Repo](../assets/docs-images/fork_repo.png)

*Fork EVA repository to your account*

### Python Version
![Python Version](../assets/docs-images/python_version.png)

*Check Python version compatibility*

### Virtual Environment
![Virtual Env](../assets/docs-images/virtual_env.jpg)

*Create and activate Python virtual environment*

### VS Code Reopen in Container
![Reopen Container](../assets/docs-images/vscode_reopen_in_container.png)

*Open project in development container*

### Starting Dev Container
![Starting Container](../assets/docs-images/vscode_starting_dev_container.png)

*Development container initialization*

### VS Code Terminal (Windows)
![Terminal Windows](../assets/docs-images/vscode_terminal_windows.png)

*Integrated terminal for Windows development*

---

**Asset Source**: Real local setup from EVA-JP-reference local repository
"""
        (dev_path / "local.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/development/local.md (with local setup assets)")
    
    def _generate_debugging_guide(self, docs_path: Path):
        """Generate debugging/debug-guide.md with debugging screenshots"""
        debug_path = docs_path / "debugging"
        debug_path.mkdir(parents=True, exist_ok=True)
        
        content = """# Debugging Guide

## Debugging Screenshots

### FastAPI Debug
![FastAPI Debug](../assets/docs-images/fastapi_debug.png)

*Backend API debugging with breakpoints*

### Frontend Watch Mode
![Frontend Watch](../assets/docs-images/frontend-watch.png)

*Hot-reload development for frontend*

### Function Attach
![Function Attach](../assets/docs-images/function_attach.png)

*Attach debugger to Azure Functions*

### Function Running
![Function Running](../assets/docs-images/function_running.png)

*Azure Functions execution status*

### Vite Debug
![Vite Debug](../assets/docs-images/vite-debug.png)

*Vite development server debugging*

### WebApp Backend Debug
![WebApp Backend](../assets/docs-images/webapp-backend.png)

*Backend web app debugging*

### WebApp Debug Configuration 1
![WebApp Debug 1](../assets/docs-images/webapp_debug_1.png)

*Debug launch configuration*

### WebApp Debug Configuration 2
![WebApp Debug 2](../assets/docs-images/webapp_debug_2.png)

*Additional debug settings*

### WebApp Debug Configuration 3
![WebApp Debug 3](../assets/docs-images/webapp_debug_3.png)

*Advanced debugging options*

### Known Issues - Web App Authentication
![Known Issues Auth](../assets/docs-images/known_Issues_web_app_authentication.png)

*Common authentication troubleshooting*

---

**Asset Source**: Real debugging screenshots from EVA-JP-reference local repository
"""
        (debug_path / "debug-guide.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/debugging/debug-guide.md (with debugging assets)")
    
    def _generate_ops_runbook(self, docs_path: Path):
        """Generate ops/runbook.md"""
        ops_path = docs_path / "ops"
        ops_path.mkdir(parents=True, exist_ok=True)
        
        content = """# Runbook

## Typical checks

- Is the site reachable?
- Are CSS/JS assets loading?
- Do deep-links work?
- Does search work (if enabled)?

## Known hosting pitfalls to test

1. SharePoint downloads `.html` instead of rendering
2. CSS blocked or not served with correct MIME types
3. Relative paths broken when hosted in a document library subfolder
"""
        (ops_path / "runbook.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/ops/runbook.md")
    
    def _generate_library_index(self, docs_path: Path):
        """Generate library/index.md - EVA Library homepage"""
        library_path = docs_path / "library"
        library_path.mkdir(parents=True, exist_ok=True)
        
        content = """# EVA Library

Welcome to the **EVA Library** - a curated collection of EVA Books documenting the EVA ecosystem architecture, operations, and best practices.

## What is an EVA Book?

An **EVA Book** is a comprehensive documentation artifact that:
- Combines multiple markdown chapters into a cohesive narrative
- Includes PDF exports for offline reading and official distribution
- Maintains version control for iterative refinement
- Serves as authoritative reference for EVA development and operations

---

## EVA Books Collection

### 📘 EVA Tech Design & ConOps v0.2 (March 2025)

**Full Title**: EVA Foundation - Technical Design and Concept of Operations  
**Version**: 0.2 (Published March 2025)  
**Status**: Reference Documentation

[View EVA Book →](techdes-conops.md)

**Contents**:
- Source Summary & Context
- Architecture Principles
- EVA Chat Requirements
- EVA Data Assistant Requirements  
- Security, Audit & Operations
- Testing & Prioritization Strategy
- Copilot Integration Guidelines

**Formats Available**:
- 📄 PDF: `AICoE_PROJ_EVAFoundation_TechDesConOps_v.02.pdf`
- 📝 Markdown Chapters: 7 individual `.md` files
- 🤖 Copilot Context: `copilot-system.md`, `COPILOT_GUARDRAILS.md`

---

## How to Use EVA Books

### For Developers
- Reference architectural decisions and design patterns
- Understand system requirements and constraints
- Review security and operational guidelines
- Follow Copilot integration best practices

### For Operations Teams
- Use as authoritative source for deployment procedures
- Reference audit and compliance requirements
- Follow operational runbooks and troubleshooting guides

### For Documentation Contributors
- Study structure and formatting standards
- Use as template for future EVA Books
- Maintain consistency with established patterns

---

## EVA Library Structure

```
assets/reference-docs/
└── techdes-conops-v02/
    ├── 00_source_summary.md
    ├── 01_scope_and_context.md
    ├── 02_architecture_principles.md
    ├── 03_eva_chat_requirements.md
    ├── 04_eva_da_requirements.md
    ├── 05_security_audit_ops.md
    ├── 06_testing_prioritization.md
    ├── AICoE_PROJ_EVAFoundation_TechDesConOps_v.02.pdf
    ├── copilot-system.md
    └── COPILOT_GUARDRAILS.md
```

---

## Upcoming EVA Books

Future additions to the EVA Library will include:
- **EVA Deployment Guide** - Complete Azure infrastructure setup
- **EVA Developer Handbook** - Local development workflows
- **EVA Governance Playbook** - Audit, compliance, and security operations
- **EVA Integration Patterns** - SharePoint, Teams, and enterprise systems

---

**Note**: This is a living library. EVA Books are updated iteratively based on production experience and community feedback.
"""
        (library_path / "index.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/library/index.md (EVA Library homepage)")
    
    def _generate_library_techdes_conops(self, docs_path: Path):
        """Generate library/techdes-conops.md - Tech Design & ConOps EVA Book"""
        library_path = docs_path / "library"
        library_path.mkdir(parents=True, exist_ok=True)
        
        content = """# EVA Book: Technical Design & ConOps v0.2

**Full Title**: EVA Foundation - Technical Design and Concept of Operations  
**Version**: 0.2  
**Published**: March 2025  
**Authors**: AICoE EVA Foundation Team  
**Owner**: Marco Presta

---

## Document Overview

This EVA Book documents the architectural decisions, technical design, and operational concepts for the EVA Foundation ecosystem. It serves as the authoritative reference for:

- System architecture and component design
- Security and compliance requirements
- Operational procedures and runbooks
- Development guidelines and best practices
- Copilot integration patterns

---

## Chapter Structure

### 📄 [00. Source Summary](../assets/reference-docs/techdes-conops-v02/00_source_summary.md)

**Purpose**: Consolidates source documents and establishes context

**Key Topics**:
- Document provenance and versioning
- Relationship to other EVA documentation
- Scope boundaries and assumptions

---

### 📄 [01. Scope and Context](../assets/reference-docs/techdes-conops-v02/01_scope_and_context.md)

**Purpose**: Defines what EVA is, what it solves, and who it serves

**Key Topics**:
- EVA mission and vision
- Problem statement and use cases
- Stakeholder analysis
- System boundaries and interfaces

---

### 📄 [02. Architecture Principles](../assets/reference-docs/techdes-conops-v02/02_architecture_principles.md)

**Purpose**: Establishes non-negotiable architectural decisions

**Key Topics**:
- Security-first design principles
- Scalability and performance requirements
- Integration patterns and standards
- Technology stack rationale

---

### 📄 [03. EVA Chat Requirements](../assets/reference-docs/techdes-conops-v02/03_eva_chat_requirements.md)

**Purpose**: Detailed requirements for EVA Chat (Jurisprudence Assistant)

**Key Topics**:
- Functional requirements (search, retrieval, citations)
- Non-functional requirements (performance, security)
- User experience specifications
- Work/Grounded, Ungrounded, and Work+Web modes

---

### 📄 [04. EVA Data Assistant Requirements](../assets/reference-docs/techdes-conops-v02/04_eva_da_requirements.md)

**Purpose**: Detailed requirements for EVA Data Assistant

**Key Topics**:
- Structured data analysis capabilities
- Math Assistant feature specifications
- Data visualization requirements
- Integration with tabular data sources

---

### 📄 [05. Security, Audit & Operations](../assets/reference-docs/techdes-conops-v02/05_security_audit_ops.md)

**Purpose**: Security, compliance, and operational guidelines

**Key Topics**:
- Authentication and authorization (Entra ID)
- Audit logging and compliance
- Operational runbooks
- Incident response procedures
- Private endpoint architecture

---

### 📄 [06. Testing & Prioritization](../assets/reference-docs/techdes-conops-v02/06_testing_prioritization.md)

**Purpose**: Testing strategy and feature prioritization framework

**Key Topics**:
- Test pyramid and coverage targets
- Functional vs non-functional testing
- Feature prioritization matrix
- Release validation criteria

---

## Copilot Integration Documents

### 🤖 [Copilot System Instructions](../assets/reference-docs/techdes-conops-v02/copilot-system.md)

**Purpose**: GitHub Copilot configuration for EVA development

**Key Topics**:
- Copilot behavior guidelines
- Code generation patterns
- EVA-specific conventions
- AI assistant best practices

---

### 🤖 [Copilot Guardrails](../assets/reference-docs/techdes-conops-v02/COPILOT_GUARDRAILS.md)

**Purpose**: Safety constraints and ethical guidelines for AI assistance

**Key Topics**:
- Content policy boundaries
- Security and privacy constraints
- Bias mitigation strategies
- Human accountability requirements

---

## PDF Reference

📄 **Complete PDF**: [AICoE_PROJ_EVAFoundation_TechDesConOps_v.02.pdf](../assets/reference-docs/techdes-conops-v02/AICoE_PROJ_EVAFoundation_TechDesConOps_v.02.pdf)

**Use Cases**:
- Offline reading and printing
- Official distribution to stakeholders
- Archival and version control
- Compliance documentation

---

## How to Navigate This EVA Book

### For Quick Reference
- Use the chapter links above to jump directly to specific topics
- Ctrl+F (Find) to search within chapters
- Bookmark frequently referenced sections

### For Comprehensive Study
- Read chapters sequentially for full context
- Follow cross-references between chapters
- Review Copilot documents for development integration

### For Implementation
- Reference architecture principles during design reviews
- Follow requirements chapters during feature development
- Use security guidelines during deployment
- Apply testing strategies during validation

---

## Version History

| Version | Date | Key Changes | Author |
|---------|------|-------------|--------|
| **0.2** | March 2025 | Architecture refinement, security hardening, Copilot integration | EVA Foundation Team |
| 0.1 | January 2025 | Initial draft | Marco Presta |

---

## Related Documentation

- [Architecture Overview](../architecture/overview.md) - High-level system architecture
- [Deployment Guide](../deployment/azure.md) - Azure infrastructure setup
- [Governance Principles](../governance/principles.md) - Compliance and audit
- [Operations Runbook](../ops/runbook.md) - Operational procedures

---

**Note**: This EVA Book is a living document. Feedback and contributions are welcome through the EVA Foundation documentation process.
"""
        (library_path / "techdes-conops.md").write_text(content, encoding='utf-8')
        print(f"[INFO] Created: docs/library/techdes-conops.md (Tech Design & ConOps EVA Book)")
    
    def _copy_library_docs(self, docs_path: Path):
        """Copy EVA Library reference documentation"""
        # Source: Project 09 Tech Design & ConOps
        source_techdes = Path(r"C:\Users\marco.presta\OneDrive - ESDC EDSC\Documents\AICOE\EVA-JP-v1.2\docs\eva-foundation\projects\09-EVA-Repo-documentation\EVA-TechDesConOps.v02")
        dest_techdes = docs_path / "assets" / "reference-docs" / "techdes-conops-v02"
        
        if source_techdes.exists():
            dest_techdes.mkdir(parents=True, exist_ok=True)
            for file in source_techdes.glob('*'):
                if file.is_file():
                    shutil.copy2(file, dest_techdes / file.name)
            file_count = len(list(dest_techdes.glob('*')))
            print(f"[INFO] Copied {file_count} files to EVA Library (Tech Design & ConOps v0.2)")
        else:
            print(f"[WARN] Tech Design & ConOps source not found: {source_techdes}")
    
    def _log_build_success(self, output_path: Path):
        """Log build success with metadata"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "component": self.component_name,
            "operation": "build_site",
            "status": "success",
            "output_path": str(output_path),
            "file_count": len(list(output_path.rglob("*"))) if output_path.exists() else 0
        }
        
        log_file = self.logs_path / f"build_success_{self.timestamp}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_entry, f, indent=2)
