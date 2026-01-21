---
name: past-paper-scraper
description: Downloads past examination papers from official PSC websites and verified sources. Respects rate limiting, honors robots.txt, and logs all scraping activities. Use this skill to populate Raw-Papers/ with PDF/HTML papers for subsequent extraction.
---

# Past Paper Scraper

Downloads past exam papers from SPSC, PPSC, and KPPSC official sources and verified secondary sources.

## MCP Integration

This skill uses the **filesystem MCP server** for read/write operations and requires web fetching capabilities.

### Required MCP Tools
- `mcp__filesystem__read_file` - Read sources-registry.json for URLs and rate limits
- `mcp__filesystem__write_file` - Save downloaded papers to Raw-Papers/
- `mcp__filesystem__create_directory` - Create year/subject subdirectories
- **Web Fetch** - Download PDFs and HTML from source URLs (via WebFetch tool or HTTP capabilities)

## Execution Steps

1. **Validate input parameters**
   - exam_type must be one of: SPSC, PPSC, KPPSC
   - year_range must be valid (e.g., "2020-2023")
   - subjects must be non-empty array

2. **Load sources-registry.json**
   ```
   Use: mcp__filesystem__read_file
   Path: question-bank/sources-registry.json
   ```
   - Parse JSON and filter sources by exam_type
   - Sort by reliability (5 → 4 → 3) for priority ordering

3. **For each year in year_range**
   - Create directory: `Raw-Papers/{exam_type}/{year}/`
   ```
   Use: mcp__filesystem__create_directory
   Path: Raw-Papers/{exam_type}/{year}
   ```

4. **For each subject in subjects**
   - Construct paper URL from source template
   - Check rate limit compliance (last_request_time + delay_seconds)
   - Download paper content
   ```
   Use: WebFetch or HTTP capability
   URL: {source.url}/{year}/{subject}.pdf
   Headers: User-Agent: {source.user_agent}
   ```
   - Wait for rate limit delay (default 2s for official, 3s for secondary)

5. **Save downloaded content**
   ```
   Use: mcp__filesystem__write_file
   Path: Raw-Papers/{exam_type}/{year}/{subject}.{extension}
   Content: Binary PDF or HTML text
   ```

6. **Log scraping activity**
   ```
   Use: mcp__filesystem__write_file (append mode)
   Path: Logs/scraper/{date}.log
   Content: Timestamp | Exam | Year | Subject | Source | Status | Error (if any)
   ```

7. **Handle failures with retry logic**
   - Initial retry delay: 5 seconds
   - Max retries: 3
   - Exponential backoff: 5s, 10s, 20s
   - Log failure after 3 attempts, continue with next paper

8. **Return download summary**

## Input Schema

```json
{
  "exam_type": {
    "type": "string",
    "required": true,
    "enum": ["SPSC", "PPSC", "KPPSC"],
    "description": "Target exam commission"
  },
  "year_range": {
    "type": "string",
    "required": true,
    "pattern": "^\\d{4}-\\d{4}$",
    "description": "Year range to download (e.g., '2020-2023')"
  },
  "subjects": {
    "type": "array",
    "required": true,
    "items": {
      "type": "string"
    },
    "minItems": 1,
    "description": "List of subjects to download (e.g., ['Pakistan Studies', 'General Knowledge'])"
  },
  "source_priority": {
    "type": "array",
    "required": false,
    "items": {
      "type": "string"
    },
    "description": "Override default source priority (optional)"
  }
}
```

## Output Schema

```json
{
  "download_summary": {
    "type": "object",
    "properties": {
      "total_attempted": "integer",
      "successful_downloads": "integer",
      "failed_downloads": "integer",
      "downloaded_files": [
        {
          "exam": "string",
          "year": "integer",
          "subject": "string",
          "source_id": "string",
          "file_path": "string",
          "file_size_bytes": "integer",
          "download_timestamp": "string (ISO 8601)"
        }
      ],
      "failed_files": [
        {
          "exam": "string",
          "year": "integer",
          "subject": "string",
          "source_id": "string",
          "error_reason": "string",
          "retry_count": "integer"
        }
      ],
      "rate_limit_compliance": {
        "total_delays_seconds": "integer",
        "average_delay_seconds": "float"
      }
    }
  },
  "execution_status": {
    "type": "enum",
    "values": ["completed", "partial_success", "failed"]
  }
}
```

## File Paths

| Operation | Path Template |
|-----------|---------------|
| Read | `question-bank/sources-registry.json` |
| Write | `Raw-Papers/{exam_type}/{year}/{subject}.{extension}` |
| Create Dir | `Raw-Papers/{exam_type}/{year}/` |
| Log | `Logs/scraper/{YYYY-MM-DD}.log` |

## Rate Limiting Strategy

| Source Reliability | Delay Between Requests | Max Requests/Hour |
|-------------------|------------------------|-------------------|
| 5 (Official) | 2 seconds | 100 |
| 4 (Verified) | 3 seconds | 100 |
| 3 (Tertiary) | 5 seconds | 50 |

**Implementation**:
- Track last_request_timestamp per source
- Calculate wait_time = (last_request + delay_seconds) - current_time
- If wait_time > 0, sleep for wait_time before next request

## Constraints

- Must respect robots.txt (check before first request to domain)
- Must use appropriate User-Agent from sources-registry.json
- Must log every download attempt (success or failure)
- Must not exceed 100 requests/hour to any single domain
- Must handle network errors gracefully (retry with exponential backoff)
- Must skip already-downloaded files (check file existence first)
- Must validate file content (non-zero size, valid format)

## Error Handling

| Condition | Response |
|-----------|----------|
| Invalid exam_type | Return error immediately |
| Source unavailable (404, 500) | Log error, try next source in priority list |
| Rate limit exceeded (429) | Wait for extended period (60s), then retry |
| Network timeout | Retry with exponential backoff (max 3 attempts) |
| Invalid file content (0 bytes) | Delete file, log error, mark as failed |
| sources-registry.json missing | Return error, cannot proceed |

## robots.txt Compliance

Before scraping each domain:
1. Fetch robots.txt from domain root
2. Parse User-agent: * and User-agent: ExamTutor-Bot sections
3. Respect Disallow directives
4. Honor Crawl-delay if specified (override default delay)
5. If robots.txt fetch fails, assume conservative delay (5s)

## Logging Format

```
2026-01-20T10:30:45Z | SPSC | 2023 | Pakistan Studies | spsc-official | SUCCESS | /Raw-Papers/SPSC/2023/pakistan-studies.pdf | 2.4MB
2026-01-20T10:30:50Z | SPSC | 2023 | General Knowledge | spsc-official | FAILED | Network timeout after 3 retries
```

## Example Invocation

```json
{
  "exam_type": "PPSC",
  "year_range": "2022-2023",
  "subjects": ["Pakistan Studies", "General Knowledge", "Current Affairs"]
}
```

Expected behavior:
- Read sources-registry.json, filter for PPSC sources
- Create directories: Raw-Papers/PPSC/2022/, Raw-Papers/PPSC/2023/
- Download 6 papers (3 subjects × 2 years)
- Respect 2s delay between requests to official PPSC site
- Log all 6 download attempts
- Return summary with success/failure counts

## Success Criteria

- All requested papers downloaded or logged as failed
- Rate limiting respected (no 429 responses)
- All downloads logged to Logs/scraper/{date}.log
- No duplicate downloads (skip existing files)
- Execution completes within reasonable time (< 5 minutes for 10 papers)
