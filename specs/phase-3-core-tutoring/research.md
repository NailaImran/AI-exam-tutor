# Phase 0 Research: Growth Engine

**Feature**: phase-3-core-tutoring
**Date**: 2026-01-30

## Research Questions

### 1. WhatsApp Business API Integration

**Decision**: Use WhatsApp Business API via MCP server

**Rationale**:
- Official Meta API ensures reliable message delivery
- Supports message templates for structured content
- Webhook support for receiving replies
- Rate limits are generous (1000 messages/day for Business accounts)

**Alternatives Considered**:
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| WhatsApp Web automation | Free, simple | Unofficial, unreliable, ToS violation | Risk of account ban |
| Twilio WhatsApp | Well-documented | Additional cost, intermediary | Direct API preferred |
| WhatsApp Business API | Official, reliable, templates | Requires Business verification | ✅ Selected |

**Implementation Notes**:
- MCP server wraps WhatsApp Cloud API
- Environment variables: WHATSAPP_PHONE_ID, WHATSAPP_ACCESS_TOKEN
- Message types: text, template (for structured questions)
- Webhook for incoming messages (reply processing)

### 2. LinkedIn API Integration

**Decision**: Use LinkedIn Share API via MCP server

**Rationale**:
- Official API for posting content
- Supports text posts with formatting
- Can include images (for ERI badges)
- Professional audience aligns with exam preparation demographic

**Alternatives Considered**:
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| Manual posting | No API needed | No automation | Defeats purpose |
| Buffer/Hootsuite | Easy scheduling | Third-party dependency, cost | Adds complexity |
| LinkedIn API direct | Full control | Requires OAuth setup | ✅ Selected |

**Implementation Notes**:
- MCP server handles OAuth token refresh
- Environment variables: LINKEDIN_ACCESS_TOKEN
- Post format: text + optional image attachment
- Rate limit: 100 posts/day (sufficient for daily question)

### 3. ERI Badge Image Generation

**Decision**: SVG template with placeholder substitution, convert to PNG

**Rationale**:
- SVG is text-based, easy to template with placeholders
- PNG output is universally shareable
- No external image generation API needed
- Consistent branding through template

**Alternatives Considered**:
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| Canvas/Pillow (Python) | Flexible | Requires Python runtime | Not Claude Code native |
| DALL-E/image AI | Dynamic designs | Cost, inconsistent output | Overkill for badges |
| HTML to image | Web standard | Requires headless browser | Complex dependency |
| SVG template | Simple, portable | Limited design flexibility | ✅ Selected |

**Template Structure**:
```svg
<svg width="400" height="200">
  <rect fill="#1a365d" width="400" height="200"/>
  <text x="200" y="60" text-anchor="middle" fill="white" font-size="24">
    Exam Readiness Index
  </text>
  <text x="200" y="120" text-anchor="middle" fill="#48bb78" font-size="48">
    {{ERI_SCORE}}
  </text>
  <text x="200" y="160" text-anchor="middle" fill="white" font-size="18">
    {{READINESS_BAND}} | {{EXAM_TYPE}}
  </text>
</svg>
```

### 4. Scheduling Approach

**Decision**: File-based schedule configuration with manual/triggered execution

**Rationale**:
- Claude Code is invoked per-session, not a persistent daemon
- File-based config allows easy inspection and modification
- Manual trigger or cron job can invoke Claude Code
- Consistent with Phase 2 file watcher pattern

**Alternatives Considered**:
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| Node.js cron daemon | Real scheduling | Requires always-on process | Not Claude Code pattern |
| OS cron + Claude CLI | True automation | Setup complexity | Possible future enhancement |
| File-based + manual | Simple, inspectable | Not truly automated | ✅ Selected for Phase 3 |

**Schedule File Format**:
```json
{
  "task_type": "daily_question",
  "schedule": {
    "hour": 8,
    "minute": 0,
    "timezone": "Asia/Karachi"
  },
  "targets": ["all_opted_in"],
  "last_run": "2026-01-30T08:00:00+05:00",
  "next_run": "2026-01-31T08:00:00+05:00"
}
```

### 5. Study Plan Generation Algorithm

**Decision**: Weak-area-weighted topic distribution with time-to-exam scaling

**Rationale**:
- Weak areas get more practice time (Constitution III: Data-Driven)
- Days until exam affects daily time allocation
- Respects student's daily_time_minutes preference
- Builds on existing weak-area-identifier skill

**Algorithm**:
1. Get weak areas from weak-area-identifier
2. Calculate total practice time available: days_remaining × daily_time_minutes
3. Allocate time per topic based on severity scores
4. Generate daily schedule with topic rotation
5. Include rest days based on consistency patterns

### 6. Approval Workflow Pattern

**Decision**: File-based workflow with needs_action/ → done/ movement

**Rationale**:
- Consistent with Phase 2 file watcher pattern
- Human reviewer can inspect files directly
- Approval/rejection recorded in file metadata
- Simple, auditable, no database needed

**Workflow States**:
```
draft → pending_approval (in needs_action/) → approved/rejected (in done/)
```

**File Naming**:
- Study plans: `{student_id}-plan-{date}.json`
- Social posts: `linkedin-{date}.json`

## Technology Decisions Summary

| Component | Technology | Status |
|-----------|------------|--------|
| WhatsApp messaging | WhatsApp Business API via MCP | Confirmed |
| LinkedIn posting | LinkedIn Share API via MCP | Confirmed |
| Image generation | SVG template → PNG | Confirmed |
| Scheduling | File-based with manual trigger | Confirmed |
| Study plan algorithm | Weak-area-weighted | Confirmed |
| Approval workflow | needs_action/ folder pattern | Confirmed |

## Dependencies

### New MCP Servers Required

1. **@anthropic-ai/mcp-server-whatsapp** (to be configured)
   - Requires: WHATSAPP_PHONE_ID, WHATSAPP_ACCESS_TOKEN
   - Tools: send_message, get_messages, send_template

2. **@anthropic-ai/mcp-server-linkedin** (to be configured)
   - Requires: LINKEDIN_ACCESS_TOKEN
   - Tools: create_post, upload_image

### External Account Setup

1. **WhatsApp Business Account**
   - Meta Business Suite account
   - Verified WhatsApp Business number
   - Message templates approved for exam questions

2. **LinkedIn Developer Account**
   - LinkedIn app registered
   - OAuth 2.0 credentials
   - Posting permissions (w_member_social)

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| WhatsApp API unavailable | Daily questions not delivered | Queue with retry, fallback to email |
| LinkedIn rate limit | Posts not published | Queue and space out, 1/day max |
| Badge generation fails | No shareable image | Text-based ERI summary fallback |
| Student timezone incorrect | Messages at wrong time | Validate timezone on registration |
| Approval backlog | Content delays | Alert if items pending > 4 hours |

## Next Steps

1. Create data-model.md with entity schemas
2. Create contract files for message templates
3. Implement skills in priority order (Stage 3A first)
4. Configure MCP servers with credentials
5. End-to-end testing with test student
