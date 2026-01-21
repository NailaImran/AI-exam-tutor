# Contract: past-paper-scraper

**Skill**: past-paper-scraper
**Version**: 1.0
**Date**: 2026-01-19

## Purpose

Downloads past exam papers from official PSC sources and secondary educational sites.

## Input Contract

```json
{
  "exam_type": {
    "type": "enum",
    "values": ["SPSC", "PPSC", "KPPSC"],
    "required": true
  },
  "year_range": {
    "type": "string",
    "pattern": "^\\d{4}-\\d{4}$",
    "required": true,
    "example": "2020-2023"
  },
  "subjects": {
    "type": "array",
    "items": "string",
    "required": true,
    "example": ["Pakistan-Studies", "General-Knowledge"]
  },
  "source_priority": {
    "type": "enum",
    "values": ["official_only", "verified", "all"],
    "default": "verified"
  }
}
```

## Output Contract

```json
{
  "scrape_results": {
    "total_papers_found": "integer",
    "total_papers_downloaded": "integer",
    "total_papers_failed": "integer",
    "papers": [
      {
        "exam_type": "string",
        "year": "integer",
        "subject": "string",
        "file_path": "string",
        "source_url": "string",
        "source_type": "official | verified | unverified",
        "download_status": "success | failed | skipped",
        "error_message": "string | null"
      }
    ]
  },
  "log_file": "string"
}
```

## MCP Tools Required

- `mcp__filesystem__write_file` - Save downloaded papers
- `mcp__filesystem__create_directory` - Create storage directories
- `mcp__filesystem__read_file` - Read source registry

## Constraints

- Maximum 100 requests per hour per domain
- Minimum 2 seconds between requests
- Must respect robots.txt
- Must preserve original filenames
