---
name: past-paper-scraper
description: Scrapes and downloads past exam papers from official PSC sources (SPSC, PPSC, KPPSC) and secondary educational sites. Use this skill when bulk-importing past papers to expand the question bank. Handles PDF downloads and HTML scraping with rate limiting and error recovery. Stores raw papers in /Raw-Papers/{Exam}/{Year}/ structure.
---

# Past Paper Scraper

Downloads past exam papers from official and secondary sources for question extraction.

## MCP Integration

This skill uses the **filesystem MCP server** for file storage and requires HTTP capabilities for web scraping.

### Required MCP Tools
- `mcp__filesystem__write_file` - Save downloaded papers
- `mcp__filesystem__create_directory` - Create storage directories
- `mcp__filesystem__read_file` - Read source registry

## Execution Steps

1. **Validate inputs**
   - exam_type must be one of: SPSC, PPSC, KPPSC
   - year_range must be valid format: YYYY-YYYY
   - subjects must be non-empty array

2. **Load source registry**
   ```
   Use: mcp__filesystem__read_file
   Path: Question-Bank-Index/sources-registry.json
   ```
   - Get URLs for specified exam type
   - Prioritize "official" sources over "verified" over "unverified"

3. **Create storage directories**
   ```
   For each year in range:
     For each subject:
       Use: mcp__filesystem__create_directory
       Path: Raw-Papers/{exam_type}/{year}/{subject}/
   ```

4. **Scrape papers**
   - For official PSC sites: Navigate to past papers section
   - Download PDFs or scrape HTML content
   - Respect rate limiting (minimum 2 seconds between requests)
   - Implement exponential backoff on failures

5. **Store raw papers**
   ```
   Use: mcp__filesystem__write_file
   Path: Raw-Papers/{exam_type}/{year}/{subject}/{filename}
   ```
   - Preserve original filename when possible
   - Add timestamp suffix if filename conflicts

6. **Log activity**
   ```
   Use: mcp__filesystem__write_file
   Path: Logs/scraper/{date}.log
   Content: Append scraping results
   ```

7. **Return structured output**

## Input Schema

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
    "description": "Start and end year, e.g., '2018-2023'"
  },
  "subjects": {
    "type": "array",
    "items": "string",
    "required": true,
    "description": "List of subjects to scrape, e.g., ['Pakistan-Studies', 'General-Knowledge']"
  },
  "source_priority": {
    "type": "enum",
    "values": ["official_only", "verified", "all"],
    "default": "verified",
    "description": "Which source types to include"
  }
}
```

## Output Schema

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
        "error_message": "string (if failed)"
      }
    ]
  },
  "log_file": "string (path to activity log)"
}
```

## Official Source URLs

| Exam   | Official URL              | Past Papers Section      |
|--------|---------------------------|--------------------------|
| SPSC   | spsc.gov.pk               | /past-papers/            |
| PPSC   | ppsc.gop.pk               | /downloads/past-papers/  |
| KPPSC  | kppsc.gov.pk              | /resources/past-papers/  |

## Rate Limiting

- Minimum 2 seconds between requests to same domain
- Exponential backoff: 5s → 10s → 30s → 60s on failures
- Maximum 3 retries per resource
- Respect robots.txt directives

## Error Handling

| Condition | Response |
|-----------|----------|
| Site unavailable (5xx) | Retry with backoff, log failure |
| Access denied (403) | Log and skip, flag for manual review |
| Not found (404) | Log and skip, continue to next |
| PDF corrupted | Save anyway, flag for extraction review |
| Rate limited (429) | Wait specified time, then retry |

## Constraints

- Must not exceed 100 requests per hour to any single domain
- Must preserve original file names when possible
- Must log all activities for audit trail
- Must respect robots.txt (check before scraping)
- Must not store credentials or authentication tokens
