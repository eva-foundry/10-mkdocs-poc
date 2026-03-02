# Getting Started

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
