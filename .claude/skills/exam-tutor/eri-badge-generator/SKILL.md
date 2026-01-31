# Skill: eri-badge-generator

**Category**: SUPPORTING (Phase 3)
**Purpose**: Generate shareable PNG badges displaying student ERI score, readiness band, and exam type

## Description

The eri-badge-generator skill creates visual badges that students can share on social media or with friends. It loads the student's current ERI, renders an SVG template with the score and band information, and outputs a PNG file with metadata. Privacy controls ensure display names are only included when the student has granted consent.

## Input

```json
{
  "student_id": "string (required)",
  "include_display_name": "boolean (optional, default: true)"
}
```

## Output

```json
{
  "success": "boolean",
  "badge_path": "string (path to generated PNG)",
  "badge_metadata": {
    "badge_id": "string badge-YYYY-MM-DD",
    "student_id": "string",
    "generated_at": "string ISO 8601",
    "eri_score": "number 0-100",
    "readiness_band": "not_ready | developing | approaching | ready | exam_ready",
    "exam_type": "SPSC | PPSC | KPPSC",
    "display_name": "string | null",
    "is_milestone": "boolean",
    "milestone_type": "reached_40 | reached_60 | reached_80 | exam_ready | null",
    "file_path": "string",
    "share_url": "string | null"
  },
  "error": "string | null"
}
```

## Workflow

### 1. Load Student Context

```
Read: memory/students/{student_id}/profile.json
Read: memory/students/{student_id}/eri.json
```

Required data:
- `profile.exam_target` - Exam type for badge
- `profile.sharing_consent.display_name` - Public name (if consented)
- `profile.sharing_consent.allow_badge_sharing` - Privacy check
- `eri.current_score` - ERI score to display
- `eri.band` - Readiness band

### 2. Privacy Check

```javascript
// Check if student allows badge sharing
if (!profile.sharing_consent.allow_badge_sharing) {
  return error("Student has not consented to badge sharing")
}

// Determine display name
let display_name = null
if (include_display_name) {
  if (profile.sharing_consent.show_full_name) {
    display_name = profile.name
  } else {
    display_name = profile.sharing_consent.display_name || "Anonymous"
  }
}
```

### 3. Determine Band Color

```javascript
const BAND_COLORS = {
  "not_ready": "#e53e3e",      // Red
  "developing": "#ed8936",     // Orange
  "approaching": "#ecc94b",    // Yellow
  "ready": "#48bb78",          // Green
  "exam_ready": "#38a169"      // Dark Green
}

const band_color = BAND_COLORS[eri.band]
```

### 4. Load SVG Template

```
Read: specs/phase-3-core-tutoring/contracts/eri-badge-template.svg
```

### 5. Substitute Placeholders

```javascript
const placeholders = {
  "{{ERI_SCORE}}": eri.current_score.toString(),
  "{{READINESS_BAND}}": formatBandLabel(eri.band),
  "{{BAND_COLOR}}": band_color,
  "{{EXAM_TYPE}}": profile.exam_target,
  "{{DISPLAY_NAME}}": display_name || "Student"
}

// Replace all placeholders in SVG
let rendered_svg = template
for (const [placeholder, value] of Object.entries(placeholders)) {
  rendered_svg = rendered_svg.replace(new RegExp(placeholder, 'g'), value)
}
```

### 6. Format Band Label

```javascript
function formatBandLabel(band) {
  const labels = {
    "not_ready": "NOT READY",
    "developing": "DEVELOPING",
    "approaching": "APPROACHING",
    "ready": "READY",
    "exam_ready": "EXAM READY"
  }
  return labels[band] || band.toUpperCase()
}
```

### 7. Check for Milestone

```javascript
function checkMilestone(eri_score, previous_badges) {
  const milestones = {
    40: "reached_40",
    60: "reached_60",
    80: "reached_80"
  }

  // Check if this score crosses a milestone threshold
  for (const [threshold, type] of Object.entries(milestones)) {
    if (eri_score >= threshold) {
      // Check if milestone was already awarded
      const already_awarded = previous_badges.some(b =>
        b.milestone_type === type
      )
      if (!already_awarded) {
        return { is_milestone: true, milestone_type: type }
      }
    }
  }

  // Special case: exam_ready band
  if (eri_score >= 80) {
    return { is_milestone: true, milestone_type: "exam_ready" }
  }

  return { is_milestone: false, milestone_type: null }
}
```

### 8. Save Badge Files

```javascript
const today = new Date().toISOString().split('T')[0]
const badge_id = `badge-${today}`

// Save rendered SVG (which can be converted to PNG by rendering engine)
const svg_path = `memory/students/${student_id}/badges/${badge_id}.svg`
write_file(svg_path, rendered_svg)

// For PNG conversion, the SVG is self-contained and can be converted
// using any SVG-to-PNG renderer (browser, librsvg, sharp, etc.)
// The file_path in metadata points to the SVG which renders as PNG-equivalent
const badge_path = `memory/students/${student_id}/badges/${badge_id}.svg`

// Save metadata
const metadata = {
  "$schema": "exam-tutor/eri-badge/v1",
  "badge_id": badge_id,
  "student_id": student_id,
  "generated_at": new Date().toISOString(),
  "eri_score": eri.current_score,
  "readiness_band": eri.band,
  "exam_type": profile.exam_target,
  "display_name": display_name,
  "is_milestone": milestone.is_milestone,
  "milestone_type": milestone.milestone_type,
  "file_path": badge_path,
  "share_url": null  // Can be populated if hosted
}

const metadata_path = `memory/students/${student_id}/badges/${badge_id}.json`
write_file(metadata_path, JSON.stringify(metadata, null, 2))
```

## Band Color Reference

| Band | Color Name | Hex Code | RGB |
|------|------------|----------|-----|
| not_ready | Red | #e53e3e | rgb(229, 62, 62) |
| developing | Orange | #ed8936 | rgb(237, 137, 54) |
| approaching | Yellow | #ecc94b | rgb(236, 201, 75) |
| ready | Green | #48bb78 | rgb(72, 187, 120) |
| exam_ready | Dark Green | #38a169 | rgb(56, 161, 105) |

## Milestone Definitions

| Milestone Type | Trigger Condition | Description |
|----------------|-------------------|-------------|
| reached_40 | ERI >= 40 (first time) | Student exits "not ready" band |
| reached_60 | ERI >= 60 (first time) | Student reaches "approaching" level |
| reached_80 | ERI >= 80 (first time) | Student reaches "ready" level |
| exam_ready | ERI >= 80 in exam_ready band | Full exam readiness achieved |

## MCP Tools Used

- `mcp__filesystem__read_file` - Load profile, ERI, SVG template
- `mcp__filesystem__write_file` - Save badge SVG and metadata JSON
- `mcp__filesystem__list_directory` - Check existing badges for milestone detection

## Validation Rules

- `eri_score` MUST be between 0 and 100
- `readiness_band` MUST be one of: not_ready, developing, approaching, ready, exam_ready
- `display_name` MUST be present if `include_display_name` is true and consent given
- Badge can only be generated if `allow_badge_sharing` is true

## Error Handling

| Error | Action |
|-------|--------|
| Student not found | Return error with student_id |
| ERI not calculated | Return error, suggest completing practice session |
| No sharing consent | Return error, explain privacy setting needed |
| SVG template missing | Return error with template path |
| Invalid ERI score | Return error with validation details |

## Example Usage

### Generate Badge with Display Name

```json
Input: {
  "student_id": "test-student",
  "include_display_name": true
}

Output: {
  "success": true,
  "badge_path": "memory/students/test-student/badges/badge-2026-01-31.svg",
  "badge_metadata": {
    "badge_id": "badge-2026-01-31",
    "student_id": "test-student",
    "generated_at": "2026-01-31T10:30:00Z",
    "eri_score": 65,
    "readiness_band": "ready",
    "exam_type": "PPSC",
    "display_name": "Fatima A.",
    "is_milestone": false,
    "milestone_type": null,
    "file_path": "memory/students/test-student/badges/badge-2026-01-31.svg",
    "share_url": null
  },
  "error": null
}
```

### Generate Anonymous Badge

```json
Input: {
  "student_id": "test-student",
  "include_display_name": false
}

Output: {
  "success": true,
  "badge_path": "memory/students/test-student/badges/badge-2026-01-31.svg",
  "badge_metadata": {
    "badge_id": "badge-2026-01-31",
    "student_id": "test-student",
    "generated_at": "2026-01-31T10:30:00Z",
    "eri_score": 65,
    "readiness_band": "ready",
    "exam_type": "PPSC",
    "display_name": null,
    "is_milestone": false,
    "milestone_type": null,
    "file_path": "memory/students/test-student/badges/badge-2026-01-31.svg",
    "share_url": null
  },
  "error": null
}
```

### Milestone Badge Detection

```json
Input: {
  "student_id": "test-student",
  "include_display_name": true
}

// Student just reached ERI 60 for first time
Output: {
  "success": true,
  "badge_path": "memory/students/test-student/badges/badge-2026-01-31.svg",
  "badge_metadata": {
    "badge_id": "badge-2026-01-31",
    "student_id": "test-student",
    "generated_at": "2026-01-31T10:30:00Z",
    "eri_score": 62,
    "readiness_band": "approaching",
    "exam_type": "PPSC",
    "display_name": "Fatima A.",
    "is_milestone": true,
    "milestone_type": "reached_60",
    "file_path": "memory/students/test-student/badges/badge-2026-01-31.svg",
    "share_url": null
  },
  "error": null
}
```

## Constitution Compliance

- **Principle IV (Privacy First)**: Only includes display name with explicit consent
- **Principle III (Data-Driven)**: Uses actual ERI score from calculations

## Related Skills

- exam-readiness-calculator (provides ERI score)
- whatsapp-message-sender (delivers milestone notifications)
- performance-tracker (triggers badge generation on ERI updates)

## SVG Template Placeholders

The SVG template at `specs/phase-3-core-tutoring/contracts/eri-badge-template.svg` uses these placeholders:

| Placeholder | Description | Example Value |
|-------------|-------------|---------------|
| `{{ERI_SCORE}}` | Numeric ERI score | 65 |
| `{{READINESS_BAND}}` | Formatted band label | READY |
| `{{BAND_COLOR}}` | Hex color for band pill | #48bb78 |
| `{{EXAM_TYPE}}` | Target exam | PPSC |
| `{{DISPLAY_NAME}}` | Student's public name | Fatima A. |
